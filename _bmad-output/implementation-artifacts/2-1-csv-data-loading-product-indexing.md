# Story 2.1: CSV Data Loading & Product Indexing

Status: done

## Story

As a **developer**,
I want **the application to load the review CSV on startup and index reviews by product_id**,
so that **all subsequent product lookups are fast O(1) operations**.

## Acceptance Criteria

1. **[x] [AC 2.1.1]** Application loads CSV from `DATA_PATH` on startup.
2. **[x] [AC 2.1.2]** Reviews are indexed in an in-memory dictionary keyed by `product_id`.
3. **[x] [AC 2.1.3]** Required columns (`product_id`, `review_text`, `rating`, `review_date`) are validated.
4. **[x] [AC 2.1.4]** Rows with empty `review_text` are dropped with a warning.
5. **[x] [AC 2.1.5]** `FileNotFoundError` is raised if the dataset is missing.

## Tasks / Subtasks

- [x] **Task 1: Enhance Data Loading Logic**
  - [x] Implement column validation in `load_reviews()`.
  - [x] Add filtering for empty `review_text`.
  - [x] Ensure O(1) indexing in the global `_reviews_by_product` store.
- [x] **Task 2: Testing**
  - [x] Add unit tests for successful load and malformed CSVs.
  - [x] Verify error handling for missing files.
