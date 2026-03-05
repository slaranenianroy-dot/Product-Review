"""
Aspect-level sentiment analysis using VADER and SpaCy for clause splitting.

Optimized for performance: pre-processes aspects and uses faster matching.
"""
from __future__ import annotations

import re
from typing import Any

import spacy
import spacy.cli
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from app.config import settings

# ---------------------------------------------------------------------------
# Lazy Loaders
# ---------------------------------------------------------------------------
_nlp = None
_sia = None

def _get_nlp():
    """Lazy load SpaCy model."""
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm", disable=["ner", "textcat"])
        except OSError:
            spacy.cli.download("en_core_web_sm")
            _nlp = spacy.load("en_core_web_sm", disable=["ner", "textcat"])
    return _nlp

def _get_analyzer() -> SentimentIntensityAnalyzer:
    global _sia
    if _sia is None:
        import nltk
        nltk.download("vader_lexicon", quiet=True)
        _sia = SentimentIntensityAnalyzer()
        # Story 3.3: Enhance lexicon for product reviews
        _sia.lexicon.update({
            "flimsy": -2.0,
            "loose": -1.5,
            "cheap": -1.5,
            "breaks": -2.5,
            "broken": -3.0,
            "slow": -1.5,
            "laggy": -2.0,
            "disappointing": -2.0,
            "junk": -3.0,
            "terrible": -3.0,
            "excellent": 3.0,
            "amazing": 3.0,
            "perfect": 3.5,
        })
    return _sia


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def classify_sentiment(score: float) -> str:
    """Map a compound score to a label."""
    if score >= settings.POSITIVE_THRESHOLD:
        return "positive"
    if score <= settings.NEGATIVE_THRESHOLD:
        return "negative"
    return "neutral"


def _split_into_clauses(text: str) -> list[str]:
    """
    Split a sentence into clauses based on coordinating conjunctions (but, however, yet).
    """
    split_pattern = r"\s+(?:but|however|yet|though|whereas|although)\s+"
    parts = re.split(split_pattern, text, flags=re.IGNORECASE)
    return [p.strip() for p in parts if p.strip()]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze_aspect_sentiment_optimized(
    processed_reviews: list[dict[str, Any]],
    aspect: str,
) -> dict[str, Any]:
    """
    Faster version that takes pre-segmented and pre-lemmatized reviews.
    """
    sia = _get_analyzer()
    nlp = _get_nlp()
    
    # Pre-process aspect lemmas once
    aspect_doc = nlp(aspect.lower())
    aspect_lemmas = [t.lemma_ for t in aspect_doc]
    
    sentence_scores: list[dict[str, Any]] = []

    for review in processed_reviews:
        for segment in review["segments"]:
            # Set intersection is very fast
            if all(al in segment["lemmas"] for al in aspect_lemmas):
                compound = sia.polarity_scores(segment["text"])["compound"]
                sentence_scores.append(
                    {
                        "sentence": segment["text"],
                        "score": compound,
                        "review_text": review["review_text"],
                        "review_id": segment["review_id"]
                    }
                )

    if not sentence_scores:
        return {
            "aspect": aspect,
            "sentiment": "neutral",
            "score": 0.0,
            "sentence_scores": [],
        }

    mean_score = sum(s["score"] for s in sentence_scores) / len(sentence_scores)
    sentiment = classify_sentiment(mean_score)

    # Sort by score descending (most positive first)
    sentence_scores.sort(key=lambda s: s["score"], reverse=True)

    return {
        "aspect": aspect,
        "sentiment": sentiment,
        "score": round(mean_score, 4),
        "sentence_scores": sentence_scores,
    }

def analyze_aspect_sentiment(
    reviews: list[dict[str, Any]],
    aspect: str,
) -> dict[str, Any]:
    """
    Legacy wrapper for backward compatibility in tests.
    Slow, but works for individual calls.
    """
    nlp = _get_nlp()
    processed = []
    for r in reviews:
        rid = r.get("review_id", "test-rid")
        item = {
            "review_id": rid,
            "review_text": r.get("review_text", ""), 
            "segments": []
        }
        sents = r.get("sentences", [])
        if not sents and item["review_text"]:
            doc = nlp(item["review_text"])
            sents = [s.text for s in doc.sents]
        for s in sents:
            clauses = _split_into_clauses(s)
            for c in clauses:
                c_doc = nlp(c.lower())
                item["segments"].append({
                    "text": c, 
                    "lemmas": {t.lemma_ for t in c_doc},
                    "review_id": rid
                })
        processed.append(item)
    return analyze_aspect_sentiment_optimized(processed, aspect)
