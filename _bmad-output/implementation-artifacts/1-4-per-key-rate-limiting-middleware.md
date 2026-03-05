# Story 1.4: Per-Key Rate Limiting Middleware

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a **API provider**,
I want **per-key rate limiting to prevent abuse**,
so that **fair usage is enforced across all API consumers**.

## Acceptance Criteria

1. **[x] [AC 1.4.1]** API calls are limited to 10 requests per minute per API key.
2. **[x] [AC 1.4.2]** Requests exceeding the limit return 429 Too Many Requests with retry-after header.
3. **[x] [AC 1.4.3]** Rate limiting is enforced per API key, not globally.
4. **[x] [AC 1.4.4]** `GET /health` endpoint is exempt from rate limiting.
5. **[x] [AC 1.4.5]** Rate limit state is maintained in-memory (no external storage needed).
6. **[x] [AC 1.4.6]** Rate limiting middleware integrates with existing authentication.

## Tasks / Subtasks

- [x] **Task 1: Implement Rate Limiting Logic**
  - [x] Create in-memory rate limiter tracking requests per API key
  - [x] Implement sliding window or token bucket algorithm
  - [x] Set limit to 10 requests per minute
- [x] **Task 2: Create Rate Limiting Middleware**
  - [x] Add middleware to FastAPI app in `app/main.py`
  - [x] Check rate limit before processing authenticated requests
  - [x] Return 429 with retry-after header when limit exceeded
- [x] **Task 3: Exempt Public Endpoints**
  - [x] Ensure `/health` bypasses rate limiting
  - [x] Apply rate limiting only to authenticated routes
- [x] **Task 4: Testing**
  - [x] Add tests for rate limit enforcement
  - [x] Test 429 responses and retry-after headers
  - [x] Verify per-key isolation

## Dev Notes

- **Algorithm:** Token bucket or sliding window for fairness
- **Storage:** In-memory (resets on server restart)
- **Headers:** Include `X-RateLimit-Remaining` and `Retry-After` for client guidance
- **Integration:** Works with existing HTTPBearer authentication

### References

- [Architecture Decision Document](file:///c:/hackathon%201/_bmad-output/planning-artifacts/architecture.md#Authentication%20&%20Security)
- [Functional Requirements](file:///c:/hackathon%201/_bmad-output/planning-artifacts/prd.md#Rate%20Limiting%20&%20Resource%20Protection)

## Dev Agent Record

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List