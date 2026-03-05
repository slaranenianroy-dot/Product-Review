"""
Text preprocessing utilities for review text.

Responsibilities:
  - HTML stripping
  - Lowercasing and normalisation
  - Sentence splitting
"""
from __future__ import annotations

import re
import html


# Pre-compiled patterns
_HTML_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s+")
_SPECIAL_CHAR_RE = re.compile(r"[^a-z0-9\s.,!?'\"-]")
# Sentence boundary: split on .!? followed by a space or end-of-string
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def clean_text(text: str) -> str:
    """Return lowercased, HTML-stripped, normalised text."""
    if not isinstance(text, str):
        return ""
    text = html.unescape(text)
    text = _HTML_TAG_RE.sub(" ", text)
    text = text.lower()
    text = _SPECIAL_CHAR_RE.sub(" ", text)
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text


def split_sentences_raw(text: str) -> list[str]:
    """Split raw text into a list of sentences without cleaning."""
    if not text:
        return []
    # Using a simple regex fallback for when SpaCy isn't needed or available
    # but for high quality, we'll use the same splitter if possible.
    sentences = _SENTENCE_SPLIT_RE.split(text)
    return [s.strip() for s in sentences if s.strip()]


def preprocess_review(raw_text: str) -> dict:
    """
    Return a dict with:
      - cleaned: full cleaned text (for overall analysis)
      - sentences: list of raw verbatim sentences (for evidence)
    """
    cleaned = clean_text(raw_text)
    # Use raw splitting for evidence integrity
    sentences = split_sentences_raw(raw_text)
    return {"cleaned": cleaned, "sentences": sentences}
