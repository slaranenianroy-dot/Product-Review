# Story 3.2: Sentence-Level Sentiment Analysis per Aspect

Status: in-progress

## Story

As a **QA lead**,
I want **each extracted aspect to have a sentiment label and numeric score**,
so that **I can quickly identify which product features are causing customer pain.**

## Acceptance Criteria

1. **[ ] [AC 3.2.1]** Calculate average sentiment score (-1.0 to 1.0) and label (positive/negative/neutral) for each aspect.
2. **[ ] [AC 3.2.2]** Support mixed-sentiment sentences by splitting into clauses (e.g., "Good screen but bad battery" should attribute positive to screen and negative to battery).
3. **[ ] [AC 3.2.3]** Rank `top_aspects` by the magnitude of their sentiment score (most polarizing first).
4. **[ ] [AC 3.2.4]** Maintain response time under 2.0s for typical datasets.

## Tasks / Subtasks

- [ ] **Task 1: Sentiment Refinement**
  - [ ] Update `app/sentiment_analyzer.py` to use SpaCy for clause splitting or smarter sentence segmenting.
  - [ ] Improve aspect matching (use SpaCy tokens/lemmas instead of simple substring matching).
- [ ] **Task 2: Insights Orchestration**
  - [ ] Modify `app/insights_engine.py` to sort `top_aspects` by absolute sentiment score.
- [ ] **Task 3: Verification**
  - [ ] Create `tests/test_sentiment_granularity.py` with mixed-sentiment examples.
  - [ ] Verify that "battery" is negative and "screen" is positive in mixed sentences.
