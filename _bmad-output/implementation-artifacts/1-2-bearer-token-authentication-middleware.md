# Story 1.2: Bearer Token Authentication Middleware

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a **developer (or API consumer)**,
I want **secure API access with Bearer token authentication**,
so that **only authorized clients can access protected endpoints**.

## Acceptance Criteria

1. **[x] [AC 1.2.1]** `GET /api/v1/products` and `POST /api/v1/insights` require valid Bearer token in Authorization header.
2. **[x] [AC 1.2.2]** Valid requests with correct API key return 200 OK.
3. **[x] [AC 1.2.3]** Requests without Authorization header return 401 Unauthorized with JSON error.
4. **[x] [AC 1.2.4]** Requests with invalid API key return 401 Unauthorized with JSON error.
5. **[x] [AC 1.2.5]** `GET /health` remains publicly accessible without authentication.
6. **[x] [AC 1.2.6]** Authentication middleware is implemented using FastAPI's HTTPBearer.

## Tasks / Subtasks

- [x] **Task 1: Implement Authentication Middleware**
  - [x] Add HTTPBearer dependency to protected routes in `app/main.py`.
  - [x] Create authentication function to validate API key against settings.
- [x] **Task 2: Update Route Definitions**
  - [x] Apply authentication dependency to `/api/v1/products` and `/api/v1/insights`.
  - [x] Ensure `/health` remains unauthenticated.
- [x] **Task 3: Error Handling**
  - [x] Return proper 401 responses for auth failures.
  - [x] Use consistent JSON error format from models.
- [x] **Task 4: Testing**
  - [x] Update tests to include valid API key in requests.
  - [x] Add tests for authentication failures.

## Dev Notes

- **Tech Stack**: FastAPI HTTPBearer, custom validation.
- **Security**: API key stored securely via environment variables.
- **Error Format**: `{"error": "UNAUTHORIZED", "message": "Invalid API key"}`
- **Public Endpoints**: Only `/health` should be unauthenticated.

### References

- [Architecture Decision Document](file:///c:/hackathon%201/_bmad-output/planning-artifacts/architecture.md#Authentication%20&%20Security)
- [Functional Requirements](file:///c:/hackathon%201/_bmad-output/planning-artifacts/prd.md#Authentication%20Model)

## Dev Agent Record

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List