---
stepsCompleted: [step-01-validate-prerequisites, step-02-design-epics, step-03-create-stories, step-04-final-validation]
inputDocuments: [prd.md, architecture.md]
---

# hackathon 1 - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for hackathon 1, decomposing the requirements from the PRD and Architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: API can accept a product_id and return structured insights including top aspects, pros, cons, and confidence scores
FR2: System can extract 3–5 top aspects (features) from a collection of product reviews using noun phrase extraction
FR3: Each aspect receives a per-aspect sentiment classification (Positive/Negative/Neutral)
FR4: System can identify and rank pros (positive aspects) and cons (negative aspects) based on frequency and sentiment strength
FR5: System can calculate and return a confidence score between 0.0–1.0 based on the number of reviews analyzed
FR6: Every pro and con returned includes a direct quote (substring match) from an original review
FR7: Every insight includes the source review_id to enable traceability and verification
FR8: System guarantees 100% evidence substring matching – no synthesized or paraphrased evidence is returned
FR9: System returns empty response for zero-review products rather than generating fabricated insights
FR10: Aspect extraction prioritizes product-relevant nouns (e.g., "battery," "screen") over generic terms
FR11: System uses sub-sentential analysis to detect negative statements within positive reviews (contextual attribution)
FR12: System measures sentiment at the sentence level within each review to capture nuanced critiques
FR13: `/health` endpoint returns `{ "status": "online" }` for system monitoring
FR14: `GET /v1/insights/{product_id}` endpoint returns insights for a valid product ID
FR15: `GET /v1/products` endpoint returns a list of all available product IDs in the dataset
FR16: API requires Bearer token authentication via `Authorization` header for all endpoints
FR17: System limits API calls to 10 requests per minute per authenticated API key
FR18: Requests exceeding rate limit receive 429 (Too Many Requests) response with retry-after header
FR19: Each request includes consistent metadata (response time, tokens used) for monitoring
FR20: System returns 404 (Not Found) when product_id doesn't exist in dataset
FR21: System returns 401 (Unauthorized) when Bearer token is missing or invalid
FR22: System returns 422 (Unprocessable Entity) for invalid query parameters
FR23: All error responses include JSON structure with `error` code and descriptive `message`
FR24: System handles empty/null review datasets gracefully without crashing
FR25: System auto-generates OpenAPI/Swagger UI at `/docs` endpoint with interactive testing
FR26: All endpoints, request/response schemas, and error codes are documented in OpenAPI format
FR27: API documentation includes examples of successful requests and error responses
FR28: Interactive Swagger UI allows testing all endpoints with sample product IDs without external tools

### NonFunctional Requirements

NFR1: All API endpoints must respond within 2.0 seconds for typical product data (1–100 reviews)
NFR2: `GET /health` endpoint must respond in <100ms for system monitoring
NFR3: `/v1/insights/{product_id}` response time must not exceed 2.0s even with 500+ reviews
NFR4: JSON response payload size must not exceed 500KB for any single product
NFR5: All API requests must include valid Bearer token; requests without valid token receive 401 response
NFR6: API keys must be stored securely (hashed, not plain text) in configuration
NFR7: Rate limiting must be enforced per API key (not globally) to prevent token abuse
NFR8: API must validate and sanitize all query parameters to prevent injection attacks
NFR9: System must maintain 100% substring matching between returned evidence and source reviews
NFR10: Every pro and con must be traceable to an actual review with a valid review_id
NFR11: System must not hallucinate or generate fake insights; zero-review products must return empty insights
NFR12: Error responses must be consistent across all endpoints with `error` code and descriptive `message`
NFR13: System must gracefully handle edge cases (empty datasets, malformed input, missing fields) without crashing
NFR14: API must support concurrent requests without performance degradation up to 10 req/sec
NFR15: System must accommodate future growth to 10x current review dataset size without database migration
NFR16: Response time must not degrade >10% if dataset size increases 10x

### Additional Requirements

- **Starter Template**: FastAPI (existing codebase in `app/main.py`) – greenfield project using FastAPI 0.115.0 + Uvicorn 0.30.6
- **Infrastructure Setup**: Docker containerization required (Dockerfile, docker-compose.yml, .env, .env.example)
- **Data Architecture**: CSV files loaded once at startup into in-memory Python dicts (pandas DataFrames); FAISS vectors in memory for evidence retrieval
- **NLP Stack**: spaCy for noun phrase aspect extraction + DistilBERT/DistilRoBERTa for sentiment analysis + FAISS for semantic evidence matching
- **Environment Configuration**: Pydantic BaseSettings with environment variable loading; API keys stored as env vars (never in code)
- **Code Quality**: PEP 8, 88-char line limit, type hints, docstrings on all public functions, Black formatting
- **Testing Infrastructure**: pytest with FastAPI TestClient; tests/ directory mirroring app structure; mock NLP/data dependencies
- **Logging**: Structured JSON logging; include request IDs, operation context, performance metrics; never log API keys
- **Implementation Sequence** (from Architecture): ① Infrastructure setup → ② Data loading → ③ Auth/security → ④ NLP pipeline → ⑤ API endpoints → ⑥ Caching/optimization

### FR Coverage Map

| FR | Epic | Brief Description |
|----|------|------------------|
| FR13 | Epic 1 | Health endpoint returns `{"status": "online"}` |
| FR16 | Epic 1 | Bearer token auth on all endpoints |
| FR21 | Epic 1 | 401 response for missing/invalid token |
| FR20 | Epic 1 | 404 for unknown product_id |
| FR22 | Epic 1 | 422 for invalid query params |
| FR23 | Epic 1 | Consistent JSON error structure |
| FR24 | Epic 1 | Graceful handling of empty datasets |
| FR17 | Epic 1 | Rate limit 10 req/min per API key |
| FR18 | Epic 1 | 429 with retry-after header |
| FR19 | Epic 1 | Request metadata (response time) |
| FR25 | Epic 1 | Auto-generate OpenAPI/Swagger at `/docs` |
| FR26 | Epic 1 | All endpoints/schemas/errors documented |
| FR27 | Epic 1 | Docs include request/response examples |
| FR28 | Epic 1 | Interactive Swagger testing without tools |
| FR15 | Epic 2 | `GET /v1/products` returns all product IDs |
| FR1  | Epic 2 | Accept product_id, return structured insights |
| FR9  | Epic 2 | Return empty response for zero-review products |
| FR5  | Epic 2 | Confidence score 0.0–1.0 based on review volume |
| FR2  | Epic 3 | Extract 3–5 top aspects via noun phrase extraction |
| FR10 | Epic 3 | Prioritize product-relevant nouns over generic terms |
| FR3  | Epic 3 | Per-aspect sentiment classification |
| FR11 | Epic 3 | Sub-sentential analysis (contextual attribution) |
| FR12 | Epic 3 | Sentence-level sentiment for nuanced critiques |
| FR4  | Epic 3 | Rank pros/cons by frequency & sentiment strength |
| FR6  | Epic 4 | Direct quote (substring match) for every pro/con |
| FR7  | Epic 4 | Source review_id for traceability |
| FR8  | Epic 4 | 100% substring matching — no synthesis |
| FR14 | Epic 4 | Full insights endpoint `GET /v1/insights/{product_id}` |

## Epic List

### Epic 1: Secure & Observable API Foundation
Developers can authenticate with the API, discover its documentation, and rely on consistent, robust error responses and rate limiting from day one. The API can be tested end-to-end via Swagger without any external tools.
**FRs covered:** FR13, FR16, FR17, FR18, FR19, FR20, FR21, FR22, FR23, FR24, FR25, FR26, FR27, FR28

### Epic 2: Product Discovery & Confidence-Aware Responses
API consumers can list all available products in the dataset and request insights for any product, receiving a well-structured response (even for products with no reviews) that includes a meaningful confidence score reflecting data density.
**FRs covered:** FR1, FR5, FR9, FR15

### Epic 3: Aspect Extraction & Sentiment Analysis
Product managers and analysts can see which specific product features (aspects) are being talked about, along with ranked pros and cons for each aspect, derived from sentence-level sentiment analysis — including hidden negatives inside positive reviews.
**FRs covered:** FR2, FR3, FR4, FR10, FR11, FR12

### Epic 4: Evidence-Backed, Zero-Hallucination Insights
Every insight returned by the API is directly traceable to a source review with a verbatim direct quote and a review ID — guaranteeing 100% verifiable, hallucination-free intelligence that teams can act on with confidence.
**FRs covered:** FR6, FR7, FR8, FR14

---

## Epic 1: Secure & Observable API Foundation

Developers can authenticate with the API, discover its documentation, and rely on consistent, robust error responses and rate limiting from day one. The API can be tested end-to-end via Swagger without any external tools.

### Story 1.1: FastAPI Project Bootstrapping & Health Endpoint

As a **developer (or hackathon judge)**,
I want the API server to start cleanly and expose a health check endpoint,
So that I can verify the service is live and operational at any time.

**Acceptance Criteria:**

**Given** the server is started with `uvicorn app.main:app --reload` from the project root
**When** I send `GET /health`
**Then** the response is `200 OK` with body `{"status": "online"}`
**And** the response time is under 100ms

**Given** the project structure follows the architecture spec (`app/main.py`, `app/config.py`, `app/models.py`, `app/data_loader.py`)
**When** the app starts
**Then** all modules import without errors and the app is ready to serve requests

---

### Story 1.2: Bearer Token Authentication Middleware

As a **developer integrating the API**,
I want the API to require a valid Bearer token on all protected endpoints,
So that only authorized clients can access product insights.

**Acceptance Criteria:**

**Given** a request is sent without an `Authorization` header
**When** any protected endpoint is called
**Then** the response is `401 Unauthorized` with body `{"error": "UNAUTHORIZED", "message": "Missing or invalid API key"}`

**Given** a request is sent with an invalid/expired token
**When** any protected endpoint is called
**Then** the response is `401 Unauthorized` with the same consistent error format

**Given** a valid Bearer token is provided in the `Authorization: Bearer <key>` header
**When** a protected endpoint is called
**Then** the request proceeds to the handler without authentication errors

**Given** the API key is configured
**When** the application starts
**Then** the key is loaded from environment variables (never hardcoded in source)

---

### Story 1.3: Consistent JSON Error Handling

As a **developer integrating the API**,
I want all error responses to follow a consistent JSON structure,
So that I can build reliable error handling in my client code without surprises.

**Acceptance Criteria:**

**Given** a request is made for a product_id that does not exist
**When** `GET /v1/insights/{product_id}` is called
**Then** the response is `404 Not Found` with body `{"error": "PRODUCT_NOT_FOUND", "message": "<human-readable description>"}`

**Given** an invalid query parameter is passed
**When** any endpoint is called
**Then** the response is `422 Unprocessable Entity` with a consistent JSON error body

**Given** any server-side error occurs during processing
**When** a request is handled
**Then** the response never exposes a raw stack trace; it returns a structured JSON error

**Given** any error response is returned
**When** inspected by the client
**Then** it always contains both `"error"` (machine-readable code) and `"message"` (human-readable description) fields

---

### Story 1.4: Per-Key Rate Limiting Middleware

As an **API operator**,
I want to limit each API key to 10 requests per minute,
So that I can prevent abuse and protect compute resources.

**Acceptance Criteria:**

**Given** a client sends 10 or fewer requests per minute using a valid API key
**When** each request is processed
**Then** all requests succeed with appropriate 200/404 responses

**Given** a client sends more than 10 requests per minute
**When** the 11th request arrives within the same minute window
**Then** the response is `429 Too Many Requests` with a `Retry-After` header indicating when the limit resets

**Given** two different API keys are used simultaneously
**When** both approach their rate limits
**Then** each key's limit is tracked independently (one key exceeding does not affect the other)

---

### Story 1.5: OpenAPI / Swagger Documentation

As a **developer or hackathon judge**,
I want interactive API documentation auto-generated at `/docs`,
So that I can discover and test all endpoints directly in the browser without Postman.

**Acceptance Criteria:**

**Given** the FastAPI app is running
**When** I navigate to `http://localhost:8000/docs`
**Then** the Swagger UI loads and displays all endpoints (`/health`, `/v1/products`, `/v1/insights/{product_id}`)

**Given** I expand an endpoint in Swagger UI
**When** I view its schema
**Then** all request parameters, response bodies, and error codes are documented with examples

**Given** I click "Try it out" on the `/v1/insights/{product_id}` endpoint in Swagger
**When** I enter a sample product_id and execute
**Then** the response is displayed inline without leaving the browser

---

## Epic 2: Product Discovery & Confidence-Aware Responses

API consumers can list all available products in the dataset and request insights for any product, receiving a well-structured response (even for products with no reviews) that includes a meaningful confidence score reflecting data density.

### Story 2.1: CSV Data Loading & Product Indexing

As a **developer**,
I want the application to load the review CSV on startup and index reviews by product_id,
So that all subsequent product lookups are fast O(1) operations.

**Acceptance Criteria:**

**Given** a valid CSV file exists at the configured `DATASET_PATH`
**When** the application starts
**Then** the CSV is loaded into an in-memory dictionary keyed by `product_id`

**Given** the CSV contains rows with columns `product_id`, `review_text`, `rating`, `review_date`
**When** data is loaded
**Then** all required columns are validated; a startup error is raised if required columns are missing

**Given** the CSV contains rows with empty `review_text`
**When** data is loaded
**Then** those rows are silently dropped with a warning log entry, and valid rows are indexed

**Given** the CSV file does not exist at startup
**When** the application attempts to load
**Then** a clear `FileNotFoundError` (or equivalent startup error) is raised, not a silent failure

---

### Story 2.2: Product Listing Endpoint (`GET /v1/products`)

As a **developer or analyst**,
I want to retrieve a list of all available product IDs in the dataset,
So that I can discover which products I can query for insights.

**Acceptance Criteria:**

**Given** the dataset is loaded with multiple products
**When** I call `GET /v1/products` with a valid Bearer token
**Then** the response is `200 OK` with a JSON array of all unique `product_id` strings, sorted alphabetically

**Given** I call `GET /v1/products` without a valid Bearer token
**When** the request is processed
**Then** the response is `401 Unauthorized`

**Given** the dataset is empty (no rows)
**When** I call `GET /v1/products`
**Then** the response is `200 OK` with an empty array `[]`

---

### Story 2.3: Insights Endpoint Shell with Confidence Score

As a **product manager**,
I want to request insights for any product_id and receive a structured response with a confidence score,
So that I know how much to trust the data before acting on it.

**Acceptance Criteria:**

**Given** a valid `product_id` with at least 1 review exists in the dataset
**When** I call `GET /v1/insights/{product_id}` with a valid Bearer token
**Then** the response is `200 OK` with a JSON object containing `product_id`, `confidence` (float 0.0–1.0), `review_count`, `top_aspects`, `pros`, `cons`, and `summary`

**Given** a `product_id` with no reviews in the dataset
**When** I call `GET /v1/insights/{product_id}`
**Then** the response is `200 OK` with `confidence: 0`, `review_count: 0`, and empty `pros`, `cons`, `top_aspects`

**Given** a `product_id` that does not exist in the dataset
**When** I call `GET /v1/insights/{product_id}`
**Then** the response is `404 Not Found` with the standard error body

**Given** a product has 1 review
**When** confidence is calculated
**Then** `confidence ≈ 0.1`; for 100 reviews `confidence ≈ 0.9` (scaled proportionally to data density)

---

## Epic 3: Aspect Extraction & Sentiment Analysis

Product managers and analysts can see which specific product features (aspects) are being talked about, along with ranked pros and cons for each aspect, derived from sentence-level sentiment analysis — including hidden negatives inside positive reviews.

### Story 3.1: Aspect Extraction via spaCy NLP

As a **product manager**,
I want the API to automatically identify the most-mentioned product features (aspects) from reviews,
So that I can see what customers are actually talking about without reading every review.

**Acceptance Criteria:**

**Given** a product has multiple reviews mentioning nouns like "battery", "screen", "charging cable"
**When** aspect extraction runs
**Then** the top 3–5 most relevant product nouns are returned as aspects

**Given** reviews contain generic terms like "product", "thing", "item"
**When** aspect extraction runs
**Then** those generic nouns are filtered out and do not appear in the top aspects

**Given** a product has fewer than 3 meaningful aspects
**When** aspect extraction runs
**Then** only the available aspects are returned (no padding with empty/fake aspects)

**Given** the NLP pipeline (spaCy) is invoked
**When** the spaCy model is not installed
**Then** the API returns a graceful error, not a crash

---

### Story 3.2: Sentence-Level Sentiment Analysis per Aspect

As a **QA lead**,
I want each extracted aspect to have a sentiment label (Positive / Negative / Neutral) and a numeric score,
So that I can quickly identify which product features are causing customer pain.

**Acceptance Criteria:**

**Given** an aspect like "battery" is identified
**When** sentiment analysis runs on the sentences mentioning "battery"
**Then** an overall sentiment (`positive`, `negative`, or `neutral`) and a numeric score (e.g., –0.8 to +0.8) are returned for that aspect

**Given** a review sentence says "The screen is beautiful but the battery drains fast"
**When** sentence-level analysis runs
**Then** "battery" receives negative sentiment and "screen" receives positive sentiment (not averaged incorrectly)

**Given** aspects are ranked in the response
**When** the `top_aspects` list is returned
**Then** aspects are ordered by absolute sentiment score magnitude (most polarizing first)

---

### Story 3.3: Contextual Attribution (Hidden Negatives in Positive Reviews)

As a **product manager**,
I want the API to detect negative statements even within highly-rated reviews,
So that I don't miss critical product flaws that customers bury inside positive feedback.

**Acceptance Criteria:**

**Given** a 5-star review says "Love the camera, but the charging port is loose"
**When** contextual attribution analysis runs
**Then** "charging port" is flagged with negative sentiment despite the high star rating

**Given** a product with 4-star average has sentiment analysis run
**When** the API response is returned
**Then** negatively-attributed aspects from positive reviews are surfaced in `cons`, not hidden

**Given** the sentiment model (DistilBERT/DistilRoBERTa) is invoked
**When** processing a batch of reviews
**Then** response time stays within the 2.0s latency budget (NFR1/NFR3)

---

### Story 3.4: Pros & Cons Ranking

As a **product manager**,
I want the API to rank the top pros and cons for a product,
So that I can immediately see the best and worst features without sorting through raw data.

**Acceptance Criteria:**

**Given** multiple reviews mention positive attributes of "display" and "build quality"
**When** pros are generated
**Then** the pros list contains ranked entries for these aspects, ordered by frequency × sentiment strength

**Given** multiple reviews mention negative attributes of "battery life" and "customer support"
**When** cons are generated
**Then** the cons list contains ranked entries for these aspects, ordered by frequency × sentiment strength

**Given** an aspect has both positive and negative mentions
**When** it appears in pros or cons
**Then** it appears in the list that reflects its dominant sentiment (not both simultaneously)

---

## Epic 4: Evidence-Backed, Zero-Hallucination Insights

Every insight returned by the API is directly traceable to a source review with a verbatim direct quote and a review ID — guaranteeing 100% verifiable, hallucination-free intelligence that teams can act on with confidence.

### Story 4.1: Substring Evidence Linking for Pros & Cons

As a **QA lead or product manager**,
I want every pro and con to include the exact verbatim quote from the source review,
So that I can instantly verify the insight is real and find the original review.

**Acceptance Criteria:**

**Given** a con is generated for "charging port is loose"
**When** the API response is returned
**Then** the `evidence` field for that con is a verbatim substring extracted directly from a source review

**Given** any pro or con in the response
**When** I search for the `evidence` text in the original dataset
**Then** it exists as an exact substring in at least one review (100% substring match guarantee)

**Given** the system cannot find a verbatim evidence quote for an insight
**When** that edge case occurs
**Then** the insight is suppressed rather than returned with synthesized or paraphrased evidence

---

### Story 4.2: Review Traceability via Source Review ID

As a **developer or compliance auditor**,
I want every evidence quote to reference the source review identifier,
So that I can retrieve the full original review context for any insight.

**Acceptance Criteria:**

**Given** a pro or con is returned with an evidence quote
**When** I inspect the response
**Then** each evidence item includes a `source_review` field (the original full review text) to confirm context

**Given** a `product_id` with multiple reviews
**When** insights are generated
**Then** evidence is drawn from different reviews (not all from one review), where possible

**Given** any evidence item in the response
**When** I verify its `source_review`
**Then** the `evidence` text is a complete substring of that `source_review` text

---

### Story 4.3: Full `/v1/insights/{product_id}` Endpoint Integration

As a **product manager**,
I want to call a single endpoint and receive fully integrated insights — aspects, sentiment, ranked pros/cons, and verbatim evidence — all in one response,
So that I can go from product ID to actionable intelligence in under 2 seconds.

**Acceptance Criteria:**

**Given** a valid `product_id` with reviews exists
**When** I call `GET /v1/insights/{product_id}` with a valid Bearer token
**Then** the response body contains: `product_id`, `top_aspects` (with sentiment scores), `pros` (with evidence), `cons` (with evidence), `confidence`, `review_count`, and `summary`

**Given** a product with 100+ reviews
**When** the endpoint is called
**Then** the complete response is returned in under 2.0 seconds (NFR1/NFR3)

**Given** all pros and cons in the response
**When** inspected for data integrity
**Then** 100% of evidence quotes are verbatim substrings of source reviews (zero hallucination)

**Given** the response is checked for payload size
**When** any product response is returned
**Then** the payload is under 500KB (NFR4)
