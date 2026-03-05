# Story 1.3: Consistent JSON Error Handling

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a **developer (or API consumer)**,
I want **consistent JSON error responses across all endpoints**,
so that **clients can reliably parse and handle API errors**.

## Acceptance Criteria

1. **[x] [AC 1.3.1]** All 404 Not Found responses return JSON `{"error": "NOT_FOUND", "message": "Resource not found"}`
2. **[x] [AC 1.3.2]** All 422 Unprocessable Entity responses return JSON with validation error details
3. **[x] [AC 1.3.3]** All 401 Unauthorized responses return JSON `{"error": "UNAUTHORIZED", "message": "Invalid API key"}`
4. **[x] [AC 1.3.4]** All 500 Internal Server Error responses return JSON `{"error": "INTERNAL_ERROR", "message": "An unexpected error occurred"}`
5. **[x] [AC 1.3.5]** Error responses maintain consistent structure and do not leak sensitive information
6. **[x] [AC 1.3.6]** Existing error handling for authentication is preserved

## Tasks / Subtasks

- [x] **Task 1: Implement Global Exception Handlers**
  - [x] Add HTTPException handler in `app/main.py` for consistent 4xx responses
  - [x] Add general exception handler for 500 errors
  - [x] Ensure handlers return proper JSON format
- [x] **Task 2: Update Route-Specific Errors**
  - [x] Ensure 404 responses for invalid product IDs use consistent format
  - [x] Update validation errors to use 422 with details
- [x] **Task 3: Test Error Scenarios**
  - [x] Add tests for 404, 422, 401, 500 error responses
  - [x] Verify error JSON structure in all cases

## Dev Notes

- **Error Structure:** `{"error": "ERROR_CODE", "message": "Human readable message"}`
- **Security:** Never expose stack traces or sensitive data in error messages
- **Consistency:** All errors should follow the same JSON schema
- **FastAPI:** Use exception handlers for global error handling

### References

- [Architecture Decision Document](file:///c:/hackathon%201/_bmad-output/planning-artifacts/architecture.md#API%20&%20Communication%20Patterns)
- [Functional Requirements](file:///c:/hackathon%201/_bmad-output/planning-artifacts/prd.md#Error%20Handling)

## Dev Agent Record

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List