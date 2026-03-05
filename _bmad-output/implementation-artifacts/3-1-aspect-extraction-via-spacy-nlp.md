# Story 3.1: Aspect Extraction via SpaCy NLP

Status: done

## Story

As a **data scientist**,
I want **to use a modern NLP library (SpaCy) for aspect extraction**,
so that **we can more accurately identify product features and group synonyms**.

## Acceptance Criteria

1. **[x] [AC 3.1.1]** Replace NLTK-based extraction with SpaCy (`en_core_web_sm`).
2. **[x] [AC 3.1.2]** Extract nouns and noun phrases as potential aspects.
3. **[x] [AC 3.1.3]** Use SpaCy lemmatization for normalized aspect names.
4. **[x] [AC 3.1.4]** Maintain existing filtering: `MIN_ASPECT_FREQUENCY`, `ASPECT_STOPWORDS`, and length checks.
5. **[x] [AC 3.1.5]** Verify that common feature names (e.g., "battery", "quality") are correctly identified in test datasets.

## Tasks / Subtasks

- [x] **Task 1: Infrastructure**
  - [x] Install `spacy` and download `en_core_web_sm`.
- [x] **Task 2: Implementation**
  - [x] Refactor `app/aspect_extractor.py` to use SpaCy.
  - [x] Update `_extract_noun_phrases` (or equivalent) to use SpaCy's `doc.noun_chunks`.
- [x] **Task 3: Verification**
  - [x] Create `tests/test_aspect_extraction_nlp.py`.
  - [x] Compare results with the previous NLTK implementation to ensure no regressions in basic detection.
