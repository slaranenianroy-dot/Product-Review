# Story 1.5: OpenAPI / Swagger Documentation

Status: done

## Story

As a **developer or hackathon judge**,
I want **interactive API documentation auto-generated at `/docs`**,
so that **I can discover and test all endpoints directly in the browser**.

## Acceptance Criteria

1. **[x] [AC 1.5.1]** Swagger UI loads at `/docs` and displays all endpoints.
2. **[x] [AC 1.5.2]** All request parameters and response bodies are documented with examples.
3. **[x] [AC 1.5.3]** All error codes (401, 404, 422, 429) are documented with their respective schemas.
4. **[x] [AC 1.5.4]** "Try it out" functionality works with the Bearer token.

## Tasks / Subtasks

- [x] **Task 1: Enhance Model Metadata**
  - [x] Add descriptions and examples to all Pydantic models in `app/models.py`.
- [x] **Task 2: Update App Metadata**
  - [x] Add detailed description and contact info to `FastAPI` instance.
  - [x] Group endpoints using tags (System, Catalog, Analysis).
- [x] **Task 3: Document Edge Cases**
  - [x] Add explicit `responses` documentation for 401, 404, 422, and 429 errors.
- [x] **Task 4: Verification**
  - [x] Verify Swagger UI is clean and self-descriptive.

## Dev Notes
- Used `json_schema_extra` for Pydantic v2 examples.
- Categorized endpoints into logical tags for better navigation.
