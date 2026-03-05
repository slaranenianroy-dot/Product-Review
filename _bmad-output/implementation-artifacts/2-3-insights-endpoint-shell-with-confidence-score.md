# Story 2.3: Insights Endpoint Shell with Confidence Score

Status: done

## Story

As a **product manager**,
I want **to request insights for any product_id and receive a structured response with a confidence score**,
so that **I know how much to trust the data before acting on it**.

## Acceptance Criteria

1. **[x] [AC 2.3.1]** `GET /api/v1/insights/{product_id}` returns `200 OK` with full insight schema.
2. **[x] [AC 2.3.2]** If no reviews exist, returns `confidence: 0`, `review_count: 0`, and empty lists.
3. **[x] [AC 2.3.3]** Returns `404 Not Found` for nonexistent product IDs.
4. **[x] [AC 2.3.4]** Confidence score is calculated logically (e.g., 1 review ≈ 0.1, 100 reviews ≈ 0.9).

## Tasks / Subtasks

- [x] **Task 1: Refactor Endpoint**
  - [x] Convert `POST /api/v1/insights` to `GET /api/v1/insights/{product_id}` in `app/main.py`.
  - [x] Update `ReviewInsightsResponse` if needed.
- [x] **Task 2: Implement Confidence Score**
  - [x] Implement volume-based confidence logic in `app/insights_engine.py`.
  - [x] Handle "insufficient data" scenarios gracefully.
- [x] **Task 3: Testing**
  - [x] Add tests for 404, empty results, and confidence scaling.
  - [x] Update dashboard and existing tests to use the new GET endpoint.
