"""
Data loading and indexing module.

Loads a CSV containing product reviews and indexes them by product_id for O(1)
lookups at request time.
"""
from __future__ import annotations

import logging
from typing import Any

import pandas as pd

from app.config import settings
from app.preprocessor import preprocess_review

logger = logging.getLogger(__name__)

# ── Module-level cache ───────────────────────────────────────────────────────
_reviews_index: dict[str, list[dict[str, Any]]] | None = None


def _validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure required columns exist and drop rows with missing review_text."""
    # Possible column mappings (Actual vs Expected)
    column_mapping = {
        'id': 'product_id',
        'productId': 'product_id',
        'reviews.text': 'review_text',
        'text': 'review_text',
        'reviews.rating': 'rating',
        'rating': 'rating',
        'score': 'rating',
        'reviews.date': 'review_date',
        'time': 'review_date'
    }
    
    # Rename columns if they exist in the dataframe
    for actual, expected in column_mapping.items():
        if actual in df.columns and expected not in df.columns:
            df = df.rename(columns={actual: expected})

    required = {"product_id", "review_text", "rating", "review_date"}
    missing = required - set(df.columns)
    if missing:
        # Special case: if 'name' exists but 'product_id' doesn't, maybe use 'name' as product_id
        if 'name' in df.columns and 'product_id' not in df.columns:
             df = df.rename(columns={'name': 'product_id'})
             missing = required - set(df.columns)

    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}. Found: {df.columns.tolist()}")

    before = len(df)
    df = df.dropna(subset=["review_text"])
    df = df[df["review_text"].astype(str).str.strip().astype(bool)]
    dropped = before - len(df)
    if dropped:
        logger.warning("Dropped %d rows with empty review_text", dropped)

    # Coerce types
    df["product_id"] = df["product_id"].astype(str).str.strip()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["review_date"] = df["review_date"].astype(str)
    return df


def load_reviews(csv_path: str | None = None) -> dict[str, list[dict[str, Any]]]:
    """
    Load reviews CSV and return a dict keyed by product_id.

    Each value is a list of dicts:
        {
          "product_id": str,
          "review_text": str,          # original text
          "rating": float | None,
          "review_date": str,
          "cleaned": str,              # preprocessed text
          "sentences": list[str]       # split sentences
        }
    """
    global _reviews_index  # noqa: PLW0603
    if _reviews_index is not None:
        return _reviews_index

    path = csv_path or settings.DATA_PATH
    logger.info("Loading reviews from %s", path)
    df = pd.read_csv(path, encoding="utf-8")
    df = _validate_dataframe(df)

    index: dict[str, list[dict[str, Any]]] = {}
    
    # Map raw product IDs to user-friendly A001, A002, etc.
    pid_mapping: dict[str, str] = {}
    next_pid_idx = 1
    
    for _, row in df.iterrows():
        raw_pid = row["product_id"]
        if raw_pid not in pid_mapping:
            pid_mapping[raw_pid] = f"A{next_pid_idx:03d}"
            next_pid_idx += 1
        pid = pid_mapping[raw_pid]
        
        # Handle review ID mapping
        rid = str(row.get("reviews.id", row.get("id", "")))
        if not rid or rid == "nan":
            # Fallback to a hash of the review text if no ID exists
            import hashlib
            rid = hashlib.md5(row["review_text"].encode()).hexdigest()[:12]
            
        processed = preprocess_review(row["review_text"])
        record = {
            "product_id": pid,
            "review_id": rid,
            "review_text": row["review_text"],
            "rating": row["rating"],
            "review_date": row["review_date"],
            "cleaned": processed["cleaned"],
            "sentences": processed["sentences"],
        }
        index.setdefault(pid, []).append(record)

    logger.info("Indexed %d products, %d total reviews", len(index), len(df))
    _reviews_index = index
    return _reviews_index


def get_reviews(product_id: str) -> list[dict[str, Any]] | None:
    """Return the list of review dicts for a product, or None if not found."""
    index = load_reviews()
    return index.get(product_id)


def get_all_product_ids() -> list[str]:
    """Return a sorted list of all product IDs in the dataset."""
    index = load_reviews()
    return sorted(index.keys())


def reset_cache() -> None:
    """Clear the in-memory cache (useful for testing)."""
    global _reviews_index  # noqa: PLW0603
    _reviews_index = None
