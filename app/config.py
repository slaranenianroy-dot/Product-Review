"""
Central configuration for the Product Review Insights API.
Uses Pydantic BaseSettings for external configuration via environment variables.
"""
from __future__ import annotations
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings and environment variables."""
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Project metadata
    PROJECT_NAME: str = "Product Review Insights API"
    VERSION: str = "1.0.0"

    # Dataset
    DATA_PATH: Path = Path("data/amazon_electronics_reviews.csv")

    # Security
    API_KEY: str = "password"  # Default for dev, override in .env

    # Noise-filtering for aspect extraction
    ASPECT_STOPWORDS: set[str] = {
        "the", "a", "an", "this", "that", "it", "i", "we", "they", "you",
        "my", "your", "our", "their", "its", "me", "him", "her", "us", "them",
        "thing", "things", "something", "anything", "everything", "nothing",
        "one", "ones", "way", "lot", "bit", "kind", "type", "part", "place",
        "product", "item", "purchase", "order", "buy", "bought", "seller",
        "review", "reviews", "reviewer", "rating", "ratings", "star", "stars",
        "price", "money", "value", "cost", "amazon", "delivery", "shipping",
        "package", "box", "time", "day", "days", "week", "weeks", "month",
        "months", "year", "hour", "hours", "minute", "minutes", "second",
        "seconds", "use", "using", "used", "work", "works", "working", "worked",
        "good", "great", "bad", "nice", "fine", "okay", "ok", "best", "worst",
        "really", "very", "much", "well", "just", "still", "even", "also",
        "would", "could", "should", "might", "will", "can", "like", "love",
        "hate", "want", "need", "think", "know", "feel", "get", "got", "make",
        "made", "come", "came", "go", "went", "problem", "issue", "issues",
        "laptop", "phone", "tablet", "device", "computer", "machine",
        "earbud", "earbuds", "headphone", "headphones", "earphone",
        "blender", "appliance", "gadget", "accessory", "electronics",
        "kindle", "fire", "echo", "alexa", "amazon", "stick", "firestick",
        "paperwhite", "voyage", "oasis", "show", "dot", "tap", "size", "color",
        "colour", "weight", "shape", "number", "level", "end", "top", "bottom",
        "side", "front", "back", "left", "right", "hand", "hands", "ear",
        "ears", "eye", "eyes", "head", "lap", "everything", "everyone",
        "anyone", "someone", "person", "people", "home", "house", "room",
        "office", "world", "life", "set", "pair", "range", "load", "line",
    }

    # Aspect extraction
    TOP_N_ASPECTS: int = 5
    MIN_ASPECT_FREQUENCY: int = 2
    MIN_ASPECT_TOKEN_LENGTH: int = 3

    # Sentiment thresholds (VADER compound score)
    POSITIVE_THRESHOLD: float = 0.05
    NEGATIVE_THRESHOLD: float = -0.05

    # Safety / confidence
    MIN_REVIEWS_FOR_ANALYSIS: int = 3
    SUFFICIENT_REVIEW_COUNT: int = 20

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 10

settings = Settings()
