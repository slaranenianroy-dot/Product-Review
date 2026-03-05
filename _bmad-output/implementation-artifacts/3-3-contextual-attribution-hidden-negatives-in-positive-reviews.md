# Story 3.3: Contextual Attribution (Hidden Negatives in Positive Reviews)

Status: in-progress

## Story

As a **product manager**,
I want **the API to detect negative statements even within highly-rated reviews**,
so that **I don't miss critical product flaws that customers bury inside positive feedback.**

## Acceptance Criteria

1. **[ ] [AC 3.3.1]** Ensure negative clauses in 5-star reviews (e.g., "Love it, but the cable is loose") are correctly attributed as negative for the relevant aspect.
2. **[ ] [AC 3.3.2]** Surface these "buried" negatives in the `cons` section of the response.
3. **[ ] [AC 3.3.3]** Integrated Transformer-based sentiment (DistilBERT/DistilRoBERTa) if required for higher accuracy, or optimize current attribution logic.
4. **[ ] [AC 3.3.4]** Maintain response time < 2.0s even with larger datasets (NFR3).

## Tasks / Subtasks

- [ ] **Task 1: Attribution logic verification**
  - [ ] Verify that current `_split_into_clauses` logic correctly handles "buried" negatives in high-rated reviews.
- [ ] **Task 2: Advanced Sentiment (Optional/Future Proof)**
  - [ ] Research/Implement DistilBERT integration via `transformers` library if environment supports it, or refine VADER with smarter context handling.
- [ ] **Task 3: Verification**
  - [ ] Create `tests/test_contextual_attribution.py` with reviews that have high ratings but negative content for specific aspects.
  - [ ] Assert that these aspects appear in `cons` despite the overall high rating of the source review.
