"""
FastAPI application — Product Review Insights API.

Endpoints
---------
POST /api/v1/insights   — analyse reviews for a given product_id
GET  /api/v1/products   — list all available product IDs
GET  /health            — liveness probe
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Depends, Security
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.data_loader import load_reviews, get_reviews, get_all_product_ids
from app.insights_engine import generate_insights
from app.rate_limiter import RateLimiter
from app.models import (
    ErrorResponse,
    HealthResponse,
    ReviewInsightsResponse,
    ReviewRequest,
)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
)
logger = logging.getLogger("app")

# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------
security = HTTPBearer(auto_error=False)
rate_limiter = RateLimiter(max_requests=10, window_seconds=60)

async def verify_api_key(
    auth: HTTPAuthorizationCredentials | None = Security(security)
) -> str:
    """Validate the Bearer token and check rate limits."""
    if not auth or auth.credentials != settings.API_KEY:
        raise StarletteHTTPException(
            status_code=401,
            detail={
                "error": "UNAUTHORIZED",
                "message": "Invalid API key" if auth else "Missing or invalid API key"
            }
        )
    
    # Check rate limit
    api_key = auth.credentials
    allowed, requests_remaining, retry_after = rate_limiter.is_allowed(api_key)
    
    if not allowed:
        raise StarletteHTTPException(
            status_code=429,
            detail={
                "error": "RATE_LIMIT_EXCEEDED",
                "message": f"Rate limit exceeded. Retry after {retry_after} seconds."
            },
            headers={"Retry-After": str(retry_after)}
        )
    
    return api_key


# ---------------------------------------------------------------------------
# Lifespan (startup / shutdown)
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Pre-load dataset and NLTK resources on startup."""
    logger.info("🚀  Starting up — loading dataset …")
    load_reviews()
    logger.info("✅  Dataset loaded successfully.")
    yield
    logger.info("👋  Shutting down.")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "## Product Review Insights API\n\n"
        "This API provides automated analysis of product reviews, extracting "
        "key features (aspects), sentiment trends, and evidence-grounded pros and cons.\n\n"
        "### Features\n"
        "- **Aspect Extraction**: Identify what customers are talking about.\n"
        "- **Sentiment Analysis**: Understand the emotional tone per aspect.\n"
        "- **Zero-Hallucination**: Every insight is backed by a verbatim quote.\n"
        "- **Security**: Protected by Bearer Token and per-key rate limiting (10 req/min).\n"
    ),
    version=settings.VERSION,
    contact={
        "name": "Dev Support",
        "url": "https://github.com/hackathon-1",
    },
    lifespan=lifespan,
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (for the dashboard)
app.mount("/static", StaticFiles(directory="static"), name="static")


# ---------------------------------------------------------------------------
# Global exception handler
# ---------------------------------------------------------------------------
@app.exception_handler(StarletteHTTPException)
async def _http_exception_handler(request, exc):  # noqa: ANN001, ARG001
    """Handle HTTP exceptions with consistent JSON format."""
    headers = {}
    
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        content = exc.detail
    else:
        # Map status codes to specific error codes
        error_code = "ERROR"
        if exc.status_code == 404:
            error_code = "NOT_FOUND"
        elif exc.status_code == 401:
            error_code = "UNAUTHORIZED"
        elif exc.status_code == 429:
            error_code = "RATE_LIMIT_EXCEEDED"
        
        content = {"error": error_code, "message": str(exc.detail)}
    
    # Preserve custom headers (like Retry-After)
    if exc.headers:
        headers.update(exc.headers)
    
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
        headers=headers,
    )


@app.exception_handler(RequestValidationError)
async def _validation_exception_handler(request, exc):  # noqa: ANN001, ARG001
    """Handle 422 validation errors."""
    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "message": "The request payload contains validation errors.",
            "details": exc.errors(),
        },
    )


@app.exception_handler(Exception)
async def _unhandled_exception_handler(request, exc):  # noqa: ANN001, ARG001
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content={"error": "INTERNAL_ERROR", "message": "An internal server error occurred."},
    )


# ---------------------------------------------------------------------------
@app.get(
    "/health", 
    response_model=HealthResponse, 
    tags=["System"],
    summary="Health Check",
    description="Liveness and readiness probe for system monitoring."
)
async def health() -> HealthResponse:
    """Check if the service is operational."""
    return HealthResponse(status="online")


@app.get("/", include_in_schema=False)
async def dashboard() -> FileResponse:
    """Serve the web dashboard."""
    return FileResponse("static/index.html")


@app.get(
    "/api/v1/products", 
    tags=["Catalog"], 
    summary="List Product IDs",
    description="Retrieve a list of all unique product identifiers available in the dataset.",
    response_model=list[str],
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized - Missing or invalid API key"},
        429: {"model": ErrorResponse, "description": "Too Many Requests - Rate limit exceeded"},
    },
    dependencies=[Depends(verify_api_key)]
)
async def list_products() -> list[str]:
    """Return all product IDs."""
    return get_all_product_ids()


@app.get(
    "/api/v1/insights/{product_id}",
    response_model=ReviewInsightsResponse,
    summary="Generate Insights",
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized - Missing or invalid API key"},
        404: {"model": ErrorResponse, "description": "Product not found in dataset"},
        422: {"model": ErrorResponse, "description": "Validation error in request payload"},
        429: {"model": ErrorResponse, "description": "Too Many Requests - Rate limit exceeded"},
    },
    tags=["Analysis"],
    dependencies=[Depends(verify_api_key)],
)
async def get_insights(product_id: str) -> ReviewInsightsResponse:
    """
    Analyse all reviews for the requested **product_id** and return
    aspect-level sentiment, evidence-grounded pros & cons, a summary,
    and a confidence score.
    """
    product_id = product_id.strip()
    logger.info("Insights requested for product_id=%s", product_id)

    reviews = get_reviews(product_id)
    if reviews is None:
        logger.warning("Product not found: %s", product_id)
        raise StarletteHTTPException(
            status_code=404,
            detail={
                "error": "NOT_FOUND",
                "message": f"Product '{product_id}' not found in the dataset.",
            },
        )

    result = generate_insights(product_id, reviews)
    return ReviewInsightsResponse(**result)
