"""
Aspect extraction module using SpaCy NLP.

Extracts the most-discussed aspects (topics/features) from a set of product
reviews using noun-chunk analysis and POS-based filtering.

Pipeline:
  1. Process each review sentence via SpaCy.
  2. Extract candidate noun-chunks and individual nouns.
  3. Lemmatize candidates and filter through:
       a) length threshold
       b) domain-agnostic stopword list (config.ASPECT_STOPWORDS)
       c) minimum document-frequency (must appear in ≥ N reviews)
  4. Rank by frequency, return top-N.
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from typing import Any

import spacy
import spacy.cli
from app.config import settings

# ---------------------------------------------------------------------------
# SpaCy Model Loading
# ---------------------------------------------------------------------------
_nlp = None

def _get_nlp():
    """Lazy load SpaCy model."""
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm", disable=["ner", "textcat"])
        except OSError:
            # Fallback if model not downloaded
            spacy.cli.download("en_core_web_sm")
            _nlp = spacy.load("en_core_web_sm", disable=["ner", "textcat"])
    return _nlp


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_candidates(sentence: str) -> list[str]:
    """
    Extract noun-based aspect candidates from a sentence using SpaCy.

    Captures:
    1. Noun chunks (e.g., "battery life")
    2. Individual nouns/proper nouns (e.g., "sound")
    """
    nlp = _get_nlp()
    doc = nlp(sentence)
    candidates: list[str] = []

    # 1. Extract noun chunks
    for chunk in doc.noun_chunks:
        # Simplify chunk: remove determiners and leading adjectives if too long
        # But generally, noun_chunks are good as-is for aspect extraction
        # We take the lemma of the chunk head or the whole chunk
        lemma_chunk = chunk.root.lemma_.lower()
        candidates.append(lemma_chunk)
        
        # Also include the full chunk lemma if it's multiple words
        if len(chunk) > 1:
            full_chunk = " ".join([t.lemma_.lower() for t in chunk if not t.is_stop])
            if full_chunk:
                candidates.append(full_chunk)

    # 2. Extract individual nouns not already in chunks (optional, but ensures coverage)
    for token in doc:
        if token.pos_ in ("NOUN", "PROPN") and not token.is_stop:
            candidates.append(token.lemma_.lower())

    return list(set(candidates))


def _is_valid_aspect(aspect: str) -> bool:
    """Apply noise-filtering rules to a candidate aspect."""
    # Length check
    if len(aspect) < settings.MIN_ASPECT_TOKEN_LENGTH:
        return False
    # Custom stopwords
    if aspect in settings.ASPECT_STOPWORDS:
        return False
    # Basic SpaCy stopword filtering is usually done in extraction, 
    # but we add a safety check here.
    # Must contain at least one alphabetic character
    if not re.search(r"[a-z]", aspect):
        return False
    # Filter out purely numeric tokens
    if aspect.replace(" ", "").isdigit():
        return False
    return True


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def extract_aspects(
    reviews: list[dict[str, Any]],
    top_n: int = settings.TOP_N_ASPECTS,
) -> list[dict[str, Any]]:
    """
    Extract the top-N aspects from a list of review dicts using SpaCy.

    Returns: [{"aspect": str, "frequency": int, "review_count": int}, ...]
    """
    # Frequency across all sentences
    aspect_freq: Counter[str] = Counter()
    # Number of distinct reviews mentioning each aspect
    aspect_review_count: dict[str, set[int]] = defaultdict(set)

    for review_idx, review in enumerate(reviews):
        seen_in_review: set[str] = set()
        # Ensure we have sentences
        sentences = review.get("sentences", [])
        if not sentences and review.get("review_text"):
            # Fallback if sentence segmentation hasn't happened
            nlp = _get_nlp()
            doc = nlp(review["review_text"])
            sentences = [sent.text for sent in doc.sents]

        for sentence in sentences:
            candidates = _extract_candidates(sentence)
            for aspect in candidates:
                if not _is_valid_aspect(aspect):
                    continue
                aspect_freq[aspect] += 1
                if aspect not in seen_in_review:
                    aspect_review_count[aspect].add(review_idx)
                    seen_in_review.add(aspect)

    # Filter by minimum document frequency
    valid_aspects = [
        a
        for a, _ in aspect_freq.most_common()
        if len(aspect_review_count.get(a, set())) >= settings.MIN_ASPECT_FREQUENCY
    ]

    top_aspects = valid_aspects[:top_n]

    return [
        {
            "aspect": a,
            "frequency": aspect_freq[a],
            "review_count": len(aspect_review_count[a]),
        }
        for a in top_aspects
    ]


def get_aspect_sentences(
    reviews: list[dict[str, Any]],
    aspect: str,
) -> list[dict[str, str]]:
    """
    Return all sentences from *reviews* that mention *aspect*.
    """
    results: list[dict[str, str]] = []
    aspect_lower = aspect.lower()
    for review in reviews:
        sentences = review.get("sentences", [])
        if not sentences and review.get("review_text"):
            nlp = _get_nlp()
            doc = nlp(review["review_text"])
            sentences = [sent.text for sent in doc.sents]
            
        for sentence in sentences:
            if aspect_lower in sentence.lower():
                results.append(
                    {
                        "sentence": sentence,
                        "review_text": review.get("review_text", ""),
                    }
                )
    return results
