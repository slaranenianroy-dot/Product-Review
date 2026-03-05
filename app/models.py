"""
Pydantic request / response schemas for the Product Review Insights API.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


# ── Request ──────────────────────────────────────────────────────────────────

class ReviewRequest(BaseModel):
    """Body of POST /api/v1/insights."""
    product_id: str = Field(
        ...,
        min_length=1,
        description="The product identifier to analyse.",
        json_schema_extra={"example": "B001"},
    )


# ── Response building blocks ─────────────────────────────────────────────────

class AspectInfo(BaseModel):
    """Sentiment information for a single product aspect (feature)."""
    aspect: str = Field(
        ..., 
        description="The extracted product feature or topic (e.g., 'battery', 'sound quality').",
        json_schema_extra={"example": "battery life"}
    )
    sentiment: str = Field(
        ..., 
        description="Overall sentiment classification: positive, negative, or neutral.",
        json_schema_extra={"example": "positive"}
    )
    score: float = Field(
        ..., 
        description="The mean sentiment score (range -1.0 to 1.0) derived from review sentences.",
        json_schema_extra={"example": 0.85}
    )


class EvidenceItem(BaseModel):
    """A specific pro or con supported by verifiable evidence from the reviews."""
    point: str = Field(
        ..., 
        description="A short, descriptive label for this insight.",
        json_schema_extra={"example": "Long battery life"}
    )
    evidence: str = Field(
        ..., 
        description="A verbatim quote extracted from an original review.",
        json_schema_extra={"example": "The battery lasts for over 2 days on a single charge."}
    )
    source_review: str = Field(
        ..., 
        description="The full original review text to provide complete context.",
        json_schema_extra={"example": "I've been using this for a week and I'm impressed. The battery lasts for over 2 days on a single charge."}
    )
    review_id: str = Field(
        ...,
        description="Verifiable source review identifier.",
        json_schema_extra={"example": "AVqkIhwDv8e3D1O-lebb"}
    )


# ── Top-level response ──────────────────────────────────────────────────────

class ReviewInsightsResponse(BaseModel):
    """Complete analysis results for a specific product."""
    product_id: str = Field(..., description="The unique identifier of the product.", json_schema_extra={"example": "B001"})
    top_aspects: list[AspectInfo] = Field(
        default_factory=list,
        description="The most discussed product features and their sentiment."
    )
    pros: list[EvidenceItem] = Field(
        default_factory=list,
        description="Ranked list of positive product attributes with evidence."
    )
    cons: list[EvidenceItem] = Field(
        default_factory=list,
        description="Ranked list of negative product attributes with evidence."
    )
    summary: str = Field(
        "", 
        description="A concise narrative summary of the overall sentiment.",
        json_schema_extra={"example": "Overall, customers are highly satisfied with the battery life and build quality, though some noted issues with the screen brightness."}
    )
    confidence: float = Field(
        ..., 
        ge=0.0, 
        le=1.0, 
        description="Statistical confidence in the results (0.0 to 1.0) based on review volume.",
        json_schema_extra={"example": 0.92}
    )
    review_count: int = Field(
        ..., 
        ge=0, 
        description="Total number of reviews processed for this analysis.",
        json_schema_extra={"example": 150}
    )


# ── Error response ──────────────────────────────────────────────────────────

class ErrorResponse(BaseModel):
    """Standard error object for all failed API requests."""
    error: str = Field(
        ..., 
        description="A unique, machine-readable error code (e.g., 'NOT_FOUND', 'UNAUTHORIZED').",
        json_schema_extra={"example": "NOT_FOUND"}
    )
    message: str = Field(
        ..., 
        description="A human-readable description of why the error occurred.",
        json_schema_extra={"example": "The requested product 'BXYZ' was not found in the dataset."}
    )

class HealthResponse(BaseModel):
    """Response payload for GET /health."""
    status: str = Field(..., description="Service status, should be 'online'.", json_schema_extra={"example": "online"})
