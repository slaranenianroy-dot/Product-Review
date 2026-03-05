"""
Insights engine — the orchestrator that wires together aspect extraction,
sentiment analysis, and evidence selection into the final API response payload.

Strict rule: **no pro or con is emitted without a supporting evidence sentence
taken verbatim from the original reviews.**
"""
from __future__ import annotations

from typing import Any

from app.config import settings
from app.aspect_extractor import extract_aspects
from app.sentiment_analyzer import (
    analyze_aspect_sentiment, 
    analyze_aspect_sentiment_optimized,
    _get_nlp,
    _split_into_clauses
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _pick_best_evidence(
    sentence_scores: list[dict[str, Any]],
    positive: bool,
) -> dict[str, str]:
    """
    Select the single best evidence sentence for a pro (positive=True) or
    con (positive=False).

    Returns {"evidence": str, "source_review": str}.
    """
    if not sentence_scores:
        return {"evidence": "", "source_review": ""}

    if positive:
        # Highest compound score
        best = max(sentence_scores, key=lambda s: s["score"])
    else:
        # Lowest compound score
        best = min(sentence_scores, key=lambda s: s["score"])

    return {
        "evidence": best["sentence"],
        "source_review": best["review_text"],
        "review_id": best["review_id"]
    }


def _generate_summary(
    product_id: str,
    reviews: list[dict[str, Any]],
    aspect_sentiments: list[dict[str, Any]],
) -> str:
    """Build a concise natural-language summary grounded in the data."""
    n = len(reviews)
    ratings = [r["rating"] for r in reviews if r.get("rating") is not None]
    avg_rating = round(sum(ratings) / len(ratings), 1) if ratings else None

    positive_aspects = [a["aspect"] for a in aspect_sentiments if a["sentiment"] == "positive"]
    negative_aspects = [a["aspect"] for a in aspect_sentiments if a["sentiment"] == "negative"]

    parts: list[str] = []
    parts.append(
        f"Based on {n} review{'s' if n != 1 else ''} for product {product_id}"
        + (f" (average rating {avg_rating}/5)" if avg_rating else "")
        + ":"
    )

    if positive_aspects:
        parts.append(
            "Reviewers praised the " + ", ".join(positive_aspects) + "."
        )
    if negative_aspects:
        parts.append(
            "Common complaints include the " + ", ".join(negative_aspects) + "."
        )
    if not positive_aspects and not negative_aspects:
        parts.append("Reviewers had mixed opinions with no strong positive or negative themes.")

    return " ".join(parts)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_insights(
    product_id: str,
    reviews: list[dict[str, Any]],
    top_n: int = settings.TOP_N_ASPECTS,
) -> dict[str, Any]:
    """
    Full insights pipeline for a product.

    Returns the final response payload dict matching the API schema.
    """
    num_reviews = len(reviews)

    # ── Confidence ───────────────────────────────────────────────────────
    # Logarithmic scaling: 1 review ≈ 0.1, 100 reviews ≈ 0.9
    import math
    if num_reviews >= 1:
        # Confidence = 0.1 + 0.4 * log10(n)
        confidence = 0.1 + 0.4 * math.log10(num_reviews)
        confidence = min(0.95, round(confidence, 2))
    else:
        confidence = 0.0

    # ── Not-enough-data safety ───────────────────────────────────────────
    if num_reviews < settings.MIN_REVIEWS_FOR_ANALYSIS:
        return {
            "product_id": product_id,
            "top_aspects": [],
            "pros": [],
            "cons": [],
            "summary": (
                f"Not enough data to generate insights for product {product_id}. "
                f"Only {num_reviews} review{'s' if num_reviews != 1 else ''} available; "
                f"at least {settings.MIN_REVIEWS_FOR_ANALYSIS} are required."
            ),
            "confidence": confidence,
            "review_count": num_reviews,
        }

    # ── Aspect extraction ────────────────────────────────────────────────
    raw_aspects = extract_aspects(reviews, top_n=top_n)
    aspect_names = [a["aspect"] for a in raw_aspects]

    # ── Pre-process Reviews (Story 3.3 Optimization) ─────────────────────
    # Process reviews into segmented clauses with lemmas once per product.
    processed_reviews = []
    nlp = _get_nlp()
    for review in reviews:
        review_id = review.get("review_id", "unknown")
        review_data = {
            "review_id": review_id,
            "review_text": review.get("review_text", ""),
            "segments": []
        }
        
        sentences = review.get("sentences", [])
        if not sentences and review_data["review_text"]:
            doc = nlp(review_data["review_text"])
            sentences = [sent.text for sent in doc.sents]
            
        for sent in sentences:
            clauses = _split_into_clauses(sent)
            for clause in clauses:
                # We analyze the clause but we keep the verbatim case for 'text'
                # so that it matches the source review exactly.
                raw_clause = clause
                clause_for_lemmas = clause.lower()
                clause_doc = nlp(clause_for_lemmas)
                
                review_data["segments"].append({
                    "text": raw_clause,
                    "lemmas": {t.lemma_ for t in clause_doc},
                    "review_id": review_id
                })
        processed_reviews.append(review_data)

    # ── Per-aspect sentiment + evidence ──────────────────────────────────
    aspect_sentiments: list[dict[str, Any]] = []
    pros: list[dict[str, Any]] = []
    cons: list[dict[str, Any]] = []

    for aspect_name in aspect_names:
        sentiment_info = analyze_aspect_sentiment_optimized(processed_reviews, aspect_name)
        evidence_sentences = sentiment_info["sentence_scores"]
        frequency = len(evidence_sentences)
        impact = round(frequency * abs(sentiment_info["score"]), 4)

        aspect_sentiments.append(
            {
                "aspect": sentiment_info["aspect"],
                "sentiment": sentiment_info["sentiment"],
                "score": sentiment_info["score"],
                "frequency": frequency,
                "impact": impact,
            }
        )

        # ── Pros: only if overall sentiment is positive AND evidence exists
        if sentiment_info["sentiment"] == "positive" and evidence_sentences:
            best = _pick_best_evidence(evidence_sentences, positive=True)
            if best["evidence"]:
                pros.append(
                    {
                        "point": f"Good {aspect_name}",
                        "evidence": best["evidence"],
                        "source_review": best["source_review"],
                        "review_id": best["review_id"],
                        "impact": impact,
                    }
                )

        # ── Cons: only if overall sentiment is negative AND evidence exists
        elif sentiment_info["sentiment"] == "negative" and evidence_sentences:
            best = _pick_best_evidence(evidence_sentences, positive=False)
            if best["evidence"]:
                cons.append(
                    {
                        "point": f"Poor {aspect_name}",
                        "evidence": best["evidence"],
                        "source_review": best["source_review"],
                        "review_id": best["review_id"],
                        "impact": impact,
                    }
                )

    # ── Sort and Limit (Story 3.4) ───────────────────────────────────────
    # Sort by impact score descending
    aspect_sentiments.sort(key=lambda a: a["impact"], reverse=True)
    pros.sort(key=lambda p: p["impact"], reverse=True)
    cons.sort(key=lambda c: c["impact"], reverse=True)

    # Limit to top_n
    top_aspects = aspect_sentiments[:top_n]
    final_pros = pros[:top_n]
    final_cons = cons[:top_n]

    # ── Summary ──────────────────────────────────────────────────────────
    summary = _generate_summary(product_id, reviews, top_aspects)

    return {
        "product_id": product_id,
        "top_aspects": top_aspects,
        "pros": final_pros,
        "cons": final_cons,
        "summary": summary,
        "confidence": confidence,
        "review_count": num_reviews,
    }
