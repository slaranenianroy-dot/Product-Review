---
stepsCompleted: [1, 2, 3, 4, 5]
inputDocuments: ["prd.md"]
workflowType: 'architecture'
project_name: 'hackathon 1'
user_name: 'LARAN ENIAN ROY'
date: '2026-03-06'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements (28 FRs):**
- Core insights generation (FR1-FR5): Product ID-based insights with aspect extraction, sentiment analysis, and confidence scoring
- Evidence integrity (FR6-FR9): 100% substring matching, review traceability, zero hallucination
- API endpoints (FR13-FR16): Health check, insights, product discovery with Bearer authentication
- Resource protection (FR17-FR19): Rate limiting, monitoring metadata
- Error handling (FR20-FR24): Comprehensive HTTP status codes with consistent JSON errors
- Developer experience (FR25-FR28): Auto-generated OpenAPI/Swagger documentation

**Non-Functional Requirements (16 NFRs):**
- Performance: <2s response time, <100ms health check, <500KB payloads
- Security: Bearer token auth, secure key storage, input validation
- Reliability: 100% data integrity, zero hallucinations, consistent error responses
- Scalability: Concurrent request support, future dataset growth accommodation

### Project Scale Assessment

**Complexity Level:** High
- 44 total requirements across functional and non-functional domains
- Strict data integrity requirements (zero hallucination, 100% traceability)
- Unstructured data processing challenges (NLP on customer reviews)
- Real-time API performance constraints (<2s latency)
- Multi-concern architecture (security, rate limiting, monitoring)

**Complexity Indicators:**
- Real-time processing: API responses must be <2s for 1-500 reviews
- Data integrity: Every insight must be substring-matched to source data
- Unstructured data: NLP processing of variable-length customer reviews
- Security: Bearer authentication with rate limiting per API key
- Scalability: Support for concurrent requests and future dataset growth

### Architectural Implications from Party Mode Analysis

**Processing Strategy:** On-demand processing for MVP with pre-computed caching for performance optimization. This balances real-time requirements with computational efficiency for evidence-based insights.

**Data Architecture:** In-memory data structures for MVP scalability, transitioning to database integration for production. Supports rapid prototyping while enabling future growth.

**Evidence Linking:** Efficient vector search using FAISS for semantic evidence matching. Critical for maintaining 100% traceability while achieving sub-2s performance.

**Scalability Considerations:** Horizontal scaling through containerization with API rate limiting. Ensures concurrent request handling and resource protection.

**Security Architecture:** Bearer token authentication with comprehensive input validation. Protects against unauthorized access and injection attacks.

**Monitoring & Observability:** Structured logging and performance metrics. Enables operational visibility and debugging for production reliability.

## Starter Template Evaluation

**Recommended Starter: FastAPI Template**

**Why FastAPI:**
- Matches your existing codebase (already implemented in app/main.py)
- Excellent for REST APIs with automatic OpenAPI/Swagger documentation
- Strong typing with Pydantic for request/response validation
- Built-in dependency injection for authentication and rate limiting
- Async support if needed for future scalability
- Active community and extensive middleware ecosystem

**Current Version:** 0.115.0 (latest stable)

**FastAPI Advantages for Your Project:**
- Native support for Bearer token authentication (matches your security requirements)
- Automatic rate limiting middleware available
- Pydantic models align perfectly with your structured JSON responses
- Built-in CORS, validation, and error handling
- Easy to add background task processing if needed

**Integration with NLP Stack:**
- Compatible with spaCy, transformers, and FAISS
- Can handle CPU-intensive NLP processing in sync endpoints
- Easy to add background pre-processing for performance

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
- Data Architecture: In-memory structures with CSV loading
- Authentication & Security: Bearer token with rate limiting
- API Design: RESTful JSON with URI versioning

**Important Decisions (Shape Architecture):**
- Processing Strategy: Synchronous with in-memory caching
- Infrastructure: Containerized deployment

**Deferred Decisions (Post-MVP):**
- Database integration for large-scale data
- OAuth2 authentication for multi-user scenarios
- Advanced monitoring and distributed tracing

### Data Architecture

**Decision:** In-memory data structures with CSV loading for MVP
**Rationale:** No database complexity needed initially - CSV loading into memory meets all current requirements while ensuring <2s response times for evidence matching. Easy transition to database when dataset grows 10x.
**Version:** N/A (Python built-in data structures)
**Implementation:** Load CSV data into pandas DataFrames on startup, use Python dicts for product indexing, FAISS vectors in memory for evidence search.
**Affects:** data_loader.py, insights_engine.py
**Provided by Starter:** No

### Authentication & Security

**Decision:** Bearer token authentication with rate limiting middleware
**Rationale:** Static API key approach matches PRD requirements without OAuth2 complexity. Per-key rate limiting prevents abuse while allowing fair usage. Establishes proper auth patterns for future enhancement.
**Version:** FastAPI HTTPBearer (built-in)
**Implementation:** HTTPBearer for token validation, custom middleware for rate limiting using in-memory tracking, API key stored as environment variable.
**Affects:** main.py, config.py
**Provided by Starter:** Partial (FastAPI provides auth framework)

### API & Communication Patterns

**Decision:** RESTful JSON API with URI versioning
**Rationale:** REST with JSON matches industry expectations for e-commerce APIs. Leverages FastAPI's strengths in auto-docs and validation. URI versioning allows clean evolution.
**Version:** OpenAPI 3.0 (FastAPI auto-generated)
**Implementation:** RESTful resource naming (/v1/insights/{product_id}), Pydantic models for schemas, automatic OpenAPI spec at /docs, consistent JSON error structure.
**Affects:** main.py, models.py
**Provided by Starter:** Yes (FastAPI provides REST framework)

### Processing & Performance

**Decision:** Synchronous processing with in-memory caching
**Rationale:** CPU-bound NLP processing doesn't benefit from async for single requests. In-memory data access ensures <2s latency. Caching optimizes for repeated product queries.
**Version:** N/A (custom implementation)
**Implementation:** Synchronous FastAPI endpoints, cached NLP results for common products, FAISS index for evidence retrieval, pandas for fast lookups.
**Affects:** insights_engine.py, aspect_extractor.py, sentiment_analyzer.py
**Provided by Starter:** No

### Infrastructure & Deployment

**Decision:** Containerized deployment with local development
**Rationale:** Docker provides consistent environments without complex infrastructure. Containerization enables horizontal scaling. Environment variables for secure configuration.
**Version:** Docker latest, Uvicorn 0.30.6
**Implementation:** Docker container with Python/FastAPI/Uvicorn, multi-stage build, environment variables for config, volume mounting for CSV data.
**Affects:** Dockerfile, docker-compose.yml, .env
**Provided by Starter:** No

### Decision Impact Analysis

**Implementation Sequence:**
1. Infrastructure setup (Docker, environment config)
2. Data loading and in-memory structures
3. Authentication and security middleware
4. Core NLP processing pipeline
5. API endpoints and response formatting
6. Performance optimization and caching

**Cross-Component Dependencies:**
- Data architecture affects all processing components
- Authentication middleware depends on configuration
- API responses depend on processing pipeline output
- Performance optimizations span data loading and NLP processing

## Implementation Patterns & Consistency Rules

### Potential Conflict Points Identified

**Naming Conflicts:**
- Variable/function naming (snake_case vs camelCase)
- Class naming conventions
- API endpoint parameter formats
- File and module naming

**Structural Conflicts:**
- Test file organization and naming
- Utility/helper function placement
- Configuration file structure
- Static data organization

**Format Conflicts:**
- API response wrapper structures
- Error response JSON formats
- Logging message formats
- Date/time serialization

**Communication Conflicts:**
- Logging level usage and message structure
- Exception handling patterns
- Configuration access patterns

**Process Conflicts:**
- Data validation timing
- Error recovery approaches
- Authentication flow implementation

### Defined Implementation Patterns

#### Naming Conventions
- **Python Code:** snake_case for variables, functions, and modules; PascalCase for classes
- **Files:** snake_case with .py extension (e.g., insights_engine.py)
- **API Endpoints:** RESTful naming with URI versioning (/v1/insights/{product_id})
- **JSON Fields:** snake_case to match Python conventions
- **Environment Variables:** UPPER_SNAKE_CASE (e.g., API_KEY, DATA_PATH)

#### Code Structure Patterns
- **Application Layout:** Standard FastAPI structure (app/ directory with main.py, models.py, etc.)
- **Test Organization:** tests/ directory with test_*.py files mirroring app structure
- **Configuration:** config.py with Pydantic BaseSettings
- **Utilities:** Helper functions in dedicated modules within app/
- **Data Loading:** data_loader.py for CSV processing and in-memory structures

#### API Response Patterns
- **Success Responses:** Direct JSON objects with snake_case fields
- **Error Responses:** Consistent format `{"error": "ERROR_CODE", "message": "Human readable message"}`
- **Pagination:** Not needed for current scope (single product responses)
- **Metadata:** Include processing timestamps and confidence scores

#### Error Handling Patterns
- **API Errors:** FastAPI HTTPException with appropriate status codes
- **Validation Errors:** Automatic Pydantic validation with 422 responses
- **Application Errors:** Custom exceptions with consistent error codes
- **Logging:** All errors logged with full context and stack traces

#### Logging Patterns
- **Logger Setup:** Python logging module with structured JSON format
- **Log Levels:** INFO for normal operations, ERROR for failures, DEBUG for development
- **Message Structure:** Include request IDs, operation context, and performance metrics
- **Sensitive Data:** Never log API keys or personal information

#### Configuration Patterns
- **Settings Class:** Pydantic BaseSettings with environment variable loading
- **Validation:** Settings validated at application startup
- **Secrets:** API keys stored as environment variables, never in code
- **Defaults:** Sensible defaults for development, required overrides for production

#### Data Processing Patterns
- **Loading:** CSV files loaded once at startup into memory structures
- **Caching:** In-memory caching for processed results with TTL
- **Validation:** Input sanitization and type checking
- **Evidence Matching:** FAISS for vector similarity, exact substring verification

#### Security Patterns
- **Authentication:** Bearer token validation on protected endpoints
- **Rate Limiting:** Per-key tracking with configurable limits
- **Input Validation:** Pydantic models for all API inputs
- **Error Messages:** Generic messages to prevent information leakage

### Consistency Rules for AI Agents

**Code Style Rules:**
- PEP 8 compliance with 88-character line length
- Type hints on all function parameters and return values
- Docstrings for all public functions and classes
- Black code formatting

**Testing Rules:**
- Unit tests for all business logic functions
- API endpoint tests with FastAPI TestClient
- Mock external dependencies (NLP models, data loading)
- Test coverage for critical paths

**Documentation Rules:**
- OpenAPI auto-generation for API documentation
- README updates for any new dependencies or setup steps
- Inline comments for complex business logic
- Architecture decision references in code comments

## Project Structure & Boundaries

### Requirements to Component Mapping

**Insights Generation (FR1-FR5):**
- Core logic → `app/insights_engine.py`
- Confidence calculation → `app/insights_engine.py`
- Aspect ranking → `app/aspect_extractor.py`

**Evidence & Data Integrity (FR6-FR9):**
- Substring matching → `app/insights_engine.py`
- Review traceability → `app/data_loader.py` and `app/models.py`
- Zero hallucination → All processing modules

**Aspect Extraction & Sentiment (FR10-FR12):**
- NLP processing → `app/aspect_extractor.py` and `app/sentiment_analyzer.py`
- Sub-sentential analysis → `app/sentiment_analyzer.py`

**API Endpoints & Access (FR13-FR16):**
- REST endpoints → `app/main.py`
- Authentication → `app/main.py` and `app/config.py`

**Rate Limiting & Resource Protection (FR17-FR19):**
- Rate limiting middleware → `app/main.py`
- Monitoring metadata → `app/main.py`

**Error Handling & Robustness (FR20-FR24):**
- HTTP status codes → `app/main.py`
- Consistent JSON errors → `app/models.py`

**API Documentation & Developer Experience (FR25-FR28):**
- OpenAPI/Swagger → Auto-generated by FastAPI
- Interactive docs → `/docs` endpoint

### Complete Project Directory Structure

```
hackathon 1/
├── app/                           # Application source code
│   ├── __init__.py               # Package initialization
│   ├── main.py                   # FastAPI app, routes, middleware
│   ├── config.py                 # Pydantic settings, environment config
│   ├── models.py                 # Pydantic models, response schemas
│   ├── data_loader.py            # CSV loading, in-memory data structures
│   ├── insights_engine.py        # Core insights orchestration
│   ├── aspect_extractor.py       # spaCy aspect extraction
│   ├── sentiment_analyzer.py     # DistilBERT sentiment analysis
│   └── __pycache__/              # Python bytecode (ignored)
├── tests/                        # Test suite
│   ├── __init__.py              # Test package initialization
│   ├── test_api.py              # API endpoint tests
│   ├── test_insights.py         # Insights logic tests
│   ├── test_nlp.py              # NLP processing tests
│   └── __pycache__/             # Test bytecode (ignored)
├── data/                        # Static data files
│   ├── amazon_electronics_reviews.csv
│   ├── Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv
│   └── reviews.csv
├── _bmad/                       # BMAD workflow artifacts
├── _bmad-output/                # Generated documentation
│   ├── planning-artifacts/
│   │   ├── prd.md
│   │   └── architecture.md
│   └── implementation-artifacts/
├── venv_fix/                    # Virtual environment (if needed)
├── static/                      # Static web assets (if added)
├── docs/                        # Additional documentation
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── Dockerfile                   # Container definition
├── docker-compose.yml           # Local development stack
├── .env                         # Environment variables (template)
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── pyrightconfig.json           # Python type checking config
└── pytest.ini                   # Test configuration
```

### Component Boundaries & Responsibilities

#### app/main.py
**Boundaries:** API layer only
- FastAPI app initialization
- Route definitions (/health, /v1/insights, /v1/products)
- Authentication middleware
- Rate limiting middleware
- Error handling and responses
**Does NOT:** Contain business logic, data processing, or NLP

#### app/insights_engine.py
**Boundaries:** Orchestration layer
- Coordinate aspect extraction and sentiment analysis
- Generate confidence scores
- Select and format evidence quotes
- Return structured insights
**Does NOT:** Load data, handle HTTP, perform raw NLP

#### app/aspect_extractor.py
**Boundaries:** NLP processing
- Extract aspects using spaCy
- Return ranked aspect lists
- Handle text preprocessing
**Does NOT:** Perform sentiment analysis, generate insights

#### app/sentiment_analyzer.py
**Boundaries:** Sentiment processing
- Analyze sentiment per aspect using DistilBERT
- Detect contextual attribution
- Return sentiment scores
**Does NOT:** Extract aspects, format responses

#### app/data_loader.py
**Boundaries:** Data access layer
- Load CSV files into memory structures
- Provide product lookup by ID
- Cache processed data
- Validate data integrity
**Does NOT:** Perform NLP, generate responses

#### app/config.py
**Boundaries:** Configuration management
- Environment variable loading
- Settings validation
- API key management
**Does NOT:** Contain business logic

#### app/models.py
**Boundaries:** Data models and schemas
- Pydantic request/response models
- Validation schemas
- Type definitions
**Does NOT:** Contain processing logic

#### tests/
**Boundaries:** Testing layer
- Unit tests for each module
- Integration tests for API
- Mock external dependencies
- Test fixtures and utilities

## Architecture Validation Results

### Coherence Validation

**Decision Compatibility:** ✅ All technology choices are compatible
- FastAPI 0.115.0 works seamlessly with spaCy, transformers, and FAISS
- Python ecosystem ensures smooth integration
- No version conflicts identified

**Pattern Consistency:** ✅ Implementation patterns align with decisions
- Naming conventions (snake_case) consistent with Python standards
- Error handling patterns leverage FastAPI's HTTPException
- Logging patterns use Python's standard logging module

**Structure Alignment:** ✅ Project structure supports all decisions
- Component boundaries clearly defined and non-overlapping
- API layer separated from business logic
- Test structure mirrors application structure

### Requirements Coverage Validation

**Functional Requirements (28/28 covered):**
- ✅ Insights generation: Mapped to insights_engine.py
- ✅ Evidence integrity: Implemented via substring matching and traceability
- ✅ API endpoints: Defined in main.py with proper authentication
- ✅ Error handling: Consistent JSON responses with appropriate status codes
- ✅ Documentation: Auto-generated OpenAPI/Swagger

**Non-Functional Requirements (16/16 covered):**
- ✅ Performance: In-memory processing ensures <2s latency
- ✅ Security: Bearer authentication with rate limiting
- ✅ Reliability: 100% data integrity through evidence verification
- ✅ Scalability: Containerization enables horizontal scaling

### Gap Analysis

**Identified Gaps:** None
- All PRD requirements have architectural support
- No missing capabilities or unsupported features
- Future extensibility built into design (database migration path, OAuth2 ready)

### Completeness Check

**Architecture Document Sections:** Complete
- ✅ Project context analysis with party mode insights
- ✅ Starter template evaluation (FastAPI selected)
- ✅ Core architectural decisions (5 categories)
- ✅ Implementation patterns and consistency rules
- ✅ Project structure and component boundaries

**Readiness for Implementation:** ✅ Ready
- Clear component responsibilities defined
- Implementation sequence established
- AI agent consistency rules provided
- All critical decisions made collaboratively