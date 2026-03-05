# Story 3.4: Pros & Cons Ranking

Status: in-progress

## Story

As a **product analyst**,
I want **the most frequently mentioned and strongly felt product features to appear at the top of the pros and cons lists**,
so that **I can focus my attention on the insights that matter most to customers.**

## Acceptance Criteria

1. **[ ] [AC 3.4.1]** Implement a weighted score for each aspect: `Impact = Frequency * |Sentiment Score|`.
2. **[ ] [AC 3.4.2]** Sort the `pros` list by `Impact` in descending order.
3. **[ ] [AC 3.4.3]** Sort the `cons` list by `Impact` in descending order.
4. **[ ] [AC 3.4.4]** Limit the final output to the top `TOP_N_ASPECTS` (configured as 5).
5. **[ ] [AC 3.4.5]** Verify that an aspect with 10 positive mentions ranks higher than one with 1 positive mention of the same strength.

## Tasks / Subtasks

- [ ] **Task 1: Ranking Logic Implementation**
  - [ ] Modify `app/insights_engine.py` to calculate the frequency-weighted impact score.
  - [ ] Apply sorting to `pros` and `cons`.
- [ ] **Task 2: Verification**
  - [ ] Create `tests/test_ranking_logic.py` to verify frequency vs strength trade-offs.
  - [ ] Assert that a high-frequency moderate-sentiment aspect can outrank a low-frequency high-sentiment aspect.
