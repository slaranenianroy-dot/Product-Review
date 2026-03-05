---
stepsCompleted:
  - step-01-init
  - step-02-discovery
  - step-02b-vision
  - step-02c-executive-summary
  - step-03-success
  - step-04-journeys
  - step-05-domain
  - step-06-innovation
  - step-07-project-type
  - step-08-scoping
  - step-09-functional
  - step-10-nonfunctional
  - step-11-polish
inputDocuments: []
workflowType: 'prd'
classification:
  projectType: "RESTful API Service (Middleware)"
  domain: "E-commerce & Consumer Intelligence"
  complexity: "high (strict data integrity, zero hallucination, unstructured data challenges)"
  projectContext: "greenfield"
---

# Product Requirements Document - hackathon 1

**Author:** LARAN ENIAN ROY
**Date:** 2026-03-05

## Executive Summary

This RESTful API service delivers an auditable, evidence-based map of product reality, transforming unstructured customer reviews into actionable intelligence for e-commerce teams. It saves product managers and QA leads 20+ hours by pinpointing specific pain points with mathematical grounding in verified review evidence, addressing the core problem of "review fatigue" where humans cannot process thousands of reviews to identify issues like battery degradation after 3 months.

### What Makes This Special

The service provides an "audit trail" where every insight includes direct quotes and review IDs for instant verification, unlike vague AI summaries. Its core insight—contextual attribution—uncovers hidden negatives in positive reviews (e.g., a 5-star rating mentioning "flimsy charging cable"), enabling data-driven decisions on product improvements, discontinuations, and marketing.

## Project Classification

- **Project Type:** RESTful API Service (Middleware)
- **Domain:** E-commerce & Consumer Intelligence
- **Complexity:** High (strict data integrity, zero hallucination, unstructured data challenges)
- **Project Context:** Greenfield

## Success Criteria

### User Success

Users experience the "aha!" moment when the API reveals non-obvious patterns with verifiable proof, such as identifying "screen flickering at 50% brightness" with 5 linked review snippets, enabling instant bug reports. Key outcomes include compressing the review analysis cycle from 4 hours to 4 seconds, providing decision clarity on which features to prioritize (e.g., focusing on hinge complaints over speaker issues), and detecting sentiment gaps where 4-star products have 80% negative sentiment on critical components.

### Business Success

Success is measured by a cost-to-value ratio where trust and efficiency drive adoption. The "hallucination-free" rate must be 100%, with every insight traceable to source data to prevent user abandonment. Operational efficiency requires processing 1,000 reviews for under $0.01 in compute/LLM costs. Insight density focuses on the ratio of total reviews to actionable insights, filtering fluff like "Great product!" to extract signals like "charging port is loose."

### Technical Success

Production-readiness ensures a 40% correctness and functionality score. Latency must be under 2.0 seconds per product_id for real-time dashboard use. Data integrity requires 100% evidence match, with every pro/con as a direct substring of the dataset. Sparse data handling demands 0% crash rate, returning clean 200 OK responses with confidence: 0 for products with no reviews. API compliance mandates OpenAPI/Swagger documentation for immediate developer adoption.

### Measurable Outcomes

- User time savings: 99% reduction in review analysis time (from 4 hours to 4 seconds)
- Decision accuracy: 95% alignment between API insights and actual product issues identified post-launch
- Business adoption: 80% user retention after first use, driven by 100% traceability
- Technical reliability: 99.9% uptime with <2s latency and zero hallucination incidents

## Product Scope

### MVP - Minimum Viable Product

Core API functionality with evidence-based insights, audit trails, and basic sentiment analysis on top aspects, ensuring 100% data integrity and <2s latency for products with sufficient reviews.

### Growth Features (Post-MVP)

Advanced contextual attribution for sentiment gaps, multi-language support, integration with e-commerce platforms, and enhanced filtering for specific user segments.

### Vision (Future)

Full AI-driven product intelligence platform with predictive analytics, automated action recommendations, and real-time review monitoring across global marketplaces.

## User Journeys

### Product Manager Journey: From Roadmap Uncertainty to Data-Driven Decisions

**Opening Scene:** Sarah, a Product Manager at a consumer electronics company, stares at her calendar for the next hardware iteration. With limited R&D budget, she needs to prioritize features that will actually move the needle, but she's drowning in conflicting feedback from sales calls and scattered review snippets.

**Rising Action:** Sarah manually reads 50 reviews a day, trying to gauge sentiment, but confirmation bias creeps in – she focuses on the loudest complaints while missing systemic issues. Her roadmap decisions feel like educated guesses rather than evidence-based choices.

**Climax:** Sarah discovers the insights API and calls GET /insights/{product_id} for their flagship laptop. The response delivers a ranked list of top aspects: "Battery life" (sentiment: -0.3), "Display quality" (sentiment: 0.2), "Build quality" (sentiment: -0.4). Each insight includes confidence scores and direct evidence quotes.

**Resolution:** With clear data showing battery and build issues as top priorities, Sarah reallocates 60% of the R&D budget to those areas. Six months later, customer satisfaction scores improve by 25%, and Sarah's roadmap decisions are backed by mathematical evidence rather than intuition.

### QA/Support Lead Journey: From Complaint Chaos to Targeted Fixes

**Opening Scene:** Mike, a QA Lead at an e-commerce company, sees a 15% spike in returns for the "Zenith Pro Tablet." The CEO demands answers by end-of-day, but Mike is overwhelmed by vague "It's broken" complaints without specifics.

**Rising Action:** Mike spends 2 hours scrolling through Amazon reviews, noting screen mentions but unsure if it's a real pattern. He compiles a manual list of issues, but without quantification, his recommendations lack credibility.

**Climax:** Mike hits the API endpoint and receives cons like "Screen Flickering" with confidence 0.89. Clicking the evidence reveals 12 reviews stating "The screen flickers when brightness is below 20%." The API provides exact failure points with direct quotes.

**Resolution:** Mike forwards the API output to the firmware team, enabling a targeted fix deployed in 48 hours. Returns drop by 40%, and Mike becomes the go-to expert for data-driven issue resolution.

### Market Researcher Journey: From Manual Analysis to Competitive Intelligence

**Opening Scene:** Alex, a market researcher for a retail analytics firm, needs to compare how their client's products stack against competitors. Currently, Alex scrapes data into messy spreadsheets, manually identifying themes across hundreds of reviews.

**Rising Action:** Alex spends days creating pivot tables and highlighting common complaints, but the process is error-prone and time-consuming. Key insights get lost in the noise of generic praise and complaints.

**Climax:** Alex uses the API to compare multiple product_ids, receiving instant pros/cons for each: Competitor A's product has strong "battery life" but weak "customer support," while their client's has excellent "durability" but poor "charging speed."

**Resolution:** Alex delivers a "market gaps" report in hours instead of days, identifying opportunities like emphasizing durability in marketing. The client gains a competitive edge, and Alex's analysis becomes the firm's gold standard.

### API Developer Journey: From Integration Headaches to Seamless Adoption

**Opening Scene:** Jordan, a developer at a dashboard company, needs to integrate a new insights API for real-time product intelligence. Past integrations have been nightmares of 500 errors, slow responses, and unclear documentation.

**Rising Action:** Jordan tests the API with edge cases – empty strings, non-existent IDs – expecting crashes. Without proper validation and documentation, integration takes days of trial and error.

**Climax:** Jordan enters a random ID and gets a clean 404 "Product Not Found" response. Valid IDs return responses in <500ms with clear JSON structure. The Swagger UI provides interactive documentation, showing all endpoints and response schemas.

**Resolution:** Integration completes in hours, not days. The API's robustness and developer experience earn Jordan's team high marks, and the dashboard now provides real-time insights that drive business decisions.

### Journey Requirements Summary

These journeys reveal requirements for: real-time API responses (<500ms), comprehensive error handling (404s for invalid IDs), evidence-based insights with confidence scores, multi-product comparison capabilities, interactive API documentation, and robust data validation to prevent crashes on edge cases.

## Innovation & Novel Patterns

### Detected Innovation Areas

**Contextual Attribution: Sub-sentential Analysis**  
Breaks from traditional sentiment analysis by detecting nuanced negatives within positive reviews. Challenges the rating-sentiment correlation by recognizing that high-star reviews often contain the most valuable technical critiques, while low-star reviews may be primarily emotional.

**Audit Trail: Groundedness Engine**  
Provides "receipts" for AI claims through deep links to original text and review IDs. Eliminates intrinsic hallucination by making every insight actionable and defensible, addressing the liability concerns in corporate environments like BFSI clients.

**Novel Tech Combination: Tristha-Lean Stack**  
Combines rule-based pre-filtering (spaCy for noun anchoring), transformer polarity analysis (DistilRoBERTa for speed), and vector comparison (FAISS for semantic evidence matching) instead of relying on a single massive LLM.

### Market Context & Competitive Landscape

| Feature | Typical AI Summary | Your Innovation API |
|---------|-------------------|---------------------|
| Verification | "Trust me, I read it." | "Here is the exact quote and review ID." |
| Granularity | Overall product sentiment | Feature-level (aspect) sentiment |
| Data Integrity | High risk of hallucination | Zero-Hallucination (fact-checked) |
| Speed/Cost | Slow, expensive LLM calls | Fast, local NLP pipeline (Thristha-optimized) |

### Validation Approach

- **Contextual Attribution**: Test on datasets with known mixed-sentiment reviews; measure accuracy in detecting hidden negatives vs. false positives
- **Audit Trail**: Implement automated verification scripts that cross-reference all outputs against source data; achieve 100% traceability in testing
- **Tech Stack**: Benchmark performance against traditional LLM approaches; validate cost savings and speed improvements on real review datasets

### Risk Mitigation

- **Fallback for Attribution**: If sub-sentential analysis proves too complex, revert to standard sentence-level sentiment as baseline
- **Audit Trail Complexity**: Start with simplified evidence linking; scale to full deep links as technology matures
- **Stack Performance**: Maintain traditional LLM as backup option if local pipeline doesn't meet accuracy thresholds

## RESTful API Specific Requirements

### Primary Endpoints

| Endpoint | Method | Purpose |
|----------|--------|----------|
| `/health` | GET | Health Check: Returns `{ "status": "online" }` for monitoring and judge verification |
| `/v1/insights/{product_id}` | GET | Main Insights: Returns structured JSON with pros, cons, confidence scores, and evidence quotes |
| `/v1/products` | GET | Discovery: Lists available `product_id`s in the dataset for easy exploration and testing |

### Authentication Model

**Strategy:** Static API Keys via Bearer Token header

- Use `Authorization: Bearer <api_key>` header for all authenticated endpoints
- Hardcode a test key in `.env` file for MVP (demonstrates security understanding without OAuth2 overhead)
- Each request validates the provided key before processing
- Invalid or missing keys return 401 Unauthorized with clear error message

### Data Formats & Versioning

**Format:** JSON only – industry standard for e-commerce intelligence APIs

**Versioning:** URI-based versioning (e.g., `/v1/...`)
- Explicit and visible in URL bar during testing
- Allows easy future versioning without breaking existing clients
- Judges can immediately see API version in requests

### Technical Guardrails

**Rate Limiting:** Implement middleware that limits requests to 10 per minute per API key
- Prevents accidental cost spikes if integration with external APIs occurs
- Returns 429 Too Many Requests with retry-after header when limit exceeded
- Provides graceful degradation under load

**Client Integration:** Provide `client_demo.py` script using `requests` library
- Demonstrates full workflow: product discovery, insights request, response parsing, evidence display
- Acts as lightweight "SDK" equivalent for hackathon evaluation
- Proves API functionality and ease of integration

### OpenAPI Documentation

- Auto-generated Swagger UI at `/docs` endpoint (FastAPI default)
- Interactive endpoint testing directly in browser
- Clear request/response schemas for all endpoints
- Error code documentation and examples

### Error Handling

- **404 Not Found:** Product ID doesn't exist in dataset
- **401 Unauthorized:** Missing or invalid API key
- **429 Too Many Requests:** Rate limit exceeded
- **400 Bad Request:** Invalid query parameters
- All errors return consistent JSON error structure with `error` and `message` fields

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

**MVP Approach:** Verified Insight Engine

Rather than competing on AI novelty, the MVP focuses on **trust and evidence**. Success is defined by taking 500 messy reviews and extracting 5 clear, evidence-backed "Truths" about a product. Every insight must be traceable to source data; verifiability is the core differentiator.

**Target Users:** Product Managers and API Developers seeking actionable, defensible product intelligence.

**Resource Requirements:** Lean team with Python/NLP expertise, FastAPI knowledge, and CSV data handling. No database or external API calls required for MVP.

### Essential User Journeys & Priority

| Priority | User Persona | MVP Goal |
|----------|--------------|----------|
| **P0** | Product Manager | Identify top 3 features to improve based on volume-weighted sentiment and evidence |
| **P0** | API Developer (Judge) | Test endpoint via Swagger/Postman with zero crashes and clear documentation |
| **P1** | QA Lead | Locate specific technical failure quotes (evidence) to verify bug reports |
| **P2** | Market Researcher | (Post-MVP) Compare sentiment gaps between two different products |

### MVP Feature Set (Phase 1)

**Core Endpoint:**
- `GET /v1/insights/{product_id}` – Returns ranked aspects with per-aspect sentiment, pros/cons, and evidence quotes

**Aspect Engine:**
- Extraction of 3–5 top "Aspects" (e.g., Battery, Screen, Price) using spaCy noun phrase extraction
- Per-aspect sentiment scoring (Positive/Negative/Neutral)
- Evidence linking: direct quote + review_id for every pro and con

**Data Integrity:**
- Confidence guardrail: score calculated from data density (0.1 for 1 review → 0.9 for 100 reviews)
- 100% substring matching – every insight is a direct substring of original reviews
- Zero hallucination guarantee

**API Robustness:**
- Clear status codes: 404 (product not found), 422 (invalid query), 401 (auth failed), 429 (rate limit)
- Auto-generated Swagger UI for interactive testing
- Consistent JSON error structure: `{ "error": "code", "message": "description" }`

### Post-MVP Features (Phase 2 & 3)

**Phase 2 (Growth Features):**
- `GET /v1/products` – List available product IDs with basic metadata
- `/health` endpoint for monitoring and judge verification
- Rate limiting (10 req/min per API key)
- Client demo script (`client_demo.py`) showcasing complete workflow

**Phase 3 (Expansion Features):**
- Multi-product comparison endpoint: `GET /v1/compare?product_a={id}&product_b={id}`
- Temporal analysis: sentiment trends for aspects over time
- Custom aspect filtering: allow users to query specific aspects
- Advanced sentiment gap detection (P2 market researcher journey)
- Dashboard integration support

### Risk Mitigation Strategy

**Technical Risks:**
- *Risk:* spaCy extraction may miss important aspects
- *Mitigation:* Fallback to high-frequency noun phrases; manual aspect list for common product domains

- *Risk:* Sentiment scoring may be inaccurate on edge cases
- *Mitigation:* Start with DistilBERT; maintain threshold for low-confidence scores; flag ambiguous cases

**Market Risks:**
- *Risk:* Judges expect advanced AI features
- *Mitigation:* Frame MVP as "trust-focused intelligence" – explain that 100% verifiable insights outweigh complex black-box AI

**Resource Risks:**
- *Risk:* Limited time (30 hours) for full implementation
- *Mitigation:* Use existing FastAPI structure; leverage pre-built spaCy models; hardcode test data initially; scale CSV loading only if time permits

### Success Definition for MVP Launch

- ✅ All P0 journeys fully functional and tested
- ✅ Zero hallucinations: 100% evidence traceability verified in QA
- ✅ <2s latency on `/v1/insights/{product_id}` for products with 1–100 reviews
- ✅ Judges can test via Swagger with no crashes on edge cases
- ✅ Clear, auto-generated API documentation
- ✅ README explains the "verified insight" philosophy and post-MVP roadmap

## Functional Requirements

### Insights Generation

- **FR1:** API can accept a product_id and return structured insights including top aspects, pros, cons, and confidence scores
- **FR2:** System can extract 3–5 top aspects (features) from a collection of product reviews using noun phrase extraction
- **FR3:** Each aspect receives a per-aspect sentiment classification (Positive/Negative/Neutral)
- **FR4:** System can identify and rank pros (positive aspects) and cons (negative aspects) based on frequency and sentiment strength
- **FR5:** System can calculate and return a confidence score between 0.0–1.0 based on the number of reviews analyzed

### Evidence & Data Integrity

- **FR6:** Every pro and con returned includes a direct quote (substring match) from an original review
- **FR7:** Every insight includes the source review_id to enable traceability and verification
- **FR8:** System guarantees 100% evidence substring matching – no synthesized or paraphrased evidence is returned
- **FR9:** System returns empty response for zero-review products rather than generating fabricated insights

### Aspect Extraction & Sentiment

- **FR10:** Aspect extraction prioritizes product-relevant nouns (e.g., "battery," "screen") over generic terms (e.g., "product," "thing")
- **FR11:** System uses sub-sentential analysis to detect negative statements within positive reviews (contextual attribution)
- **FR12:** System measures sentiment at the sentence level within each review to capture nuanced critiques

### API Endpoints & Access

- **FR13:** `/health` endpoint returns `{ "status": "online" }` for system monitoring
- **FR14:** `GET /v1/insights/{product_id}` endpoint returns insights for a valid product ID
- **FR15:** `GET /v1/products` endpoint returns a list of all available product IDs in the dataset
- **FR16:** API requires Bearer token authentication via `Authorization` header for all endpoints

### Rate Limiting & Resource Protection

- **FR17:** System limits API calls to 10 requests per minute per authenticated API key
- **FR18:** Requests exceeding rate limit receive 429 (Too Many Requests) response with retry-after header
- **FR19:** Each request includes consistent metadata (response time, tokens used) for monitoring

### Error Handling & Robustness

- **FR20:** System returns 404 (Not Found) when product_id doesn't exist in dataset
- **FR21:** System returns 401 (Unauthorized) when Bearer token is missing or invalid
- **FR22:** System returns 422 (Unprocessable Entity) for invalid query parameters
- **FR23:** All error responses include JSON structure with `error` code and descriptive `message`
- **FR24:** System handles empty/null review datasets gracefully without crashing

### API Documentation & Developer Experience

- **FR25:** System auto-generates OpenAPI/Swagger UI at `/docs` endpoint with interactive testing
- **FR26:** All endpoints, request/response schemas, and error codes are documented in OpenAPI format
- **FR27:** API documentation includes examples of successful requests and error responses
- **FR28:** Interactive Swagger UI allows testing all endpoints with sample product IDs without external tools

## Non-Functional Requirements

### Performance

- **NFR1:** All API endpoints must respond within 2.0 seconds for typical product data (1–100 reviews)
- **NFR2:** `GET /health` endpoint must respond in <100ms for system monitoring
- **NFR3:** `/v1/insights/{product_id}` response time must not exceed 2.0s even with 500+ reviews
- **NFR4:** JSON response payload size must not exceed 500KB for any single product

### Security

- **NFR5:** All API requests must include valid Bearer token in Authorization header; requests without valid token receive 401 response
- **NFR6:** API keys must be stored securely (hashed, not plain text) in configuration
- **NFR7:** Rate limiting must be enforced per API key (not globally) to prevent token abuse
- **NFR8:** API must validate and sanitize all query parameters to prevent injection attacks

### Reliability & Data Integrity

- **NFR9:** System must maintain 100% substring matching between returned evidence and source reviews (no synthesis or paraphrasing)
- **NFR10:** Every pro and con must be traceable to an actual review with a valid review_id
- **NFR11:** System must not hallucinate or generate fake insights; zero-review products must return empty insights, not fabricated data
- **NFR12:** Error responses must be consistent across all endpoints with `error` code and descriptive `message`
- **NFR13:** System must gracefully handle edge cases (empty datasets, malformed input, missing fields) without crashing

### Scalability

- **NFR14:** API must support concurrent requests without performance degradation up to 10 req/sec
- **NFR15:** System must accommodate future growth to 10x current review dataset size without database migration
- **NFR16:** Response time must not degrade >10% if dataset size increases 10x
