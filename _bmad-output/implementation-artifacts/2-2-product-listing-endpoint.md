# Story 2.2: Product Listing Endpoint (`GET /v1/products`)

Status: done

## Story

As a **developer or analyst**,
I want **to retrieve a list of all available product IDs in the dataset**,
so that **I can discover which products I can query for insights**.

## Acceptance Criteria

1. **[x] [AC 2.2.1]** `GET /api/v1/products` returns `200 OK` with JSON array of unique product IDs, sorted alphabetically.
2. **[x] [AC 2.2.2]** Request without valid token returns `401 Unauthorized`.
3. **[x] [AC 2.2.3]** Returns empty array `[]` if dataset is empty.

## Tasks / Subtasks

- [x] **Task 1: Refine Endpoint Implementation**
  - [x] Ensure the response is a naked JSON array `[]` if required by AC.
  - [x] Verify sorting is alphabetical.
- [x] **Task 2: Testing**
  - [x] Add integration tests for success, unauthorized, and empty scenarios.
