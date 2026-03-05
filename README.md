# Product Review Insights API

A FastAPI-based REST API that analyses product reviews to extract **aspect-level sentiment**, **evidence-grounded pros & cons**, a **summary**, and a **confidence score**.

> **Key guarantee:** Every pro and con is backed by a verbatim sentence from the original reviews. The system will **never** fabricate evidence.

---

## Architecture

```
POST /api/v1/insights { "product_id": "B001" }
        │
        ▼
┌──────────────────────────────────────────┐
│  Data Loader (CSV → in-memory index)     │
│  Text Preprocessor (clean, split)        │
└────────────────┬─────────────────────────┘
                 │
        ┌────────▼────────┐
        │ Aspect Extractor │  POS-tag noun-phrase chunking
        │ + Noise Filter   │  stopwords, min-freq, min-length
        └────────┬────────┘
                 │
       ┌─────────▼─────────┐
       │ Sentiment Analyzer │  VADER per-sentence scoring
       └─────────┬─────────┘
                 │
       ┌─────────▼─────────┐
       │  Insights Engine   │  pros/cons + evidence, summary,
       │                    │  confidence, not-enough-data safety
       └─────────┬─────────┘
                 │
                 ▼
       JSON Response (schema validated by Pydantic)
```

---

## Quick Start

### 1. Clone & set up

```bash
cd c:\Hackathon
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Download NLTK data (automatic on first run, or manually)

```bash
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('wordnet'); nltk.download('stopwords'); nltk.download('vader_lexicon')"
```

### 3. Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The interactive API docs are available at **http://127.0.0.1:8000/docs**.

### 4. Run tests

```bash
python -m pytest tests/test_api.py -v
```

---

## API Reference

### `GET /health`

Liveness probe.

```json
{"status": "ok"}
```

### `GET /api/v1/products`

List all product IDs in the dataset.

```json
{"product_ids": ["B001", "B002", "B003", "B004"]}
```

### `POST /api/v1/insights`

Analyse reviews for a product.

**Request:**

```bash
curl -X POST http://127.0.0.1:8000/api/v1/insights \
     -H "Content-Type: application/json" \
     -d '{"product_id": "B001"}'
```

**Response (200):**

```json
{
  "product_id": "B001",
  "top_aspects": [
    {"aspect": "battery", "sentiment": "positive", "score": 0.3245},
    {"aspect": "keyboard", "sentiment": "negative", "score": -0.6120},
    {"aspect": "screen", "sentiment": "positive", "score": 0.5891}
  ],
  "pros": [
    {
      "point": "Good battery",
      "evidence": "the battery life on this laptop is absolutely incredible.",
      "source_review": "The battery life on this laptop is absolutely incredible. I can work for 10 hours without needing to charge."
    },
    {
      "point": "Good screen",
      "evidence": "screen quality is amazing with vibrant colors.",
      "source_review": "Screen quality is amazing with vibrant colors. The display is bright and sharp even in direct sunlight."
    }
  ],
  "cons": [
    {
      "point": "Poor keyboard",
      "evidence": "the keyboard feels cheap and the keys are too small for comfortable typing.",
      "source_review": "The keyboard feels cheap and the keys are too small for comfortable typing. Very disappointing keyboard layout."
    }
  ],
  "summary": "Based on 15 reviews for product B001 (average rating 3.5/5): Reviewers praised the battery, screen. Common complaints include the keyboard.",
  "confidence": 0.75,
  "review_count": 15
}
```

**Error responses:**

| Status | Meaning |
|--------|---------|
| 404 | Product ID not found |
| 422 | Invalid / missing input |
| 500 | Internal server error |

---

## Dataset Format

The CSV must contain these columns:

| Column | Type | Description |
|--------|------|-------------|
| `product_id` | string | Unique product identifier |
| `review_text` | string | Full review text |
| `rating` | float | Star rating (1–5) |
| `review_date` | string | Date of the review |

To use your own dataset, set the `REVIEWS_CSV_PATH` environment variable:

```bash
set REVIEWS_CSV_PATH=path\to\your\reviews.csv   # Windows
uvicorn app.main:app --reload
```

Compatible datasets:
- [Amazon Product Reviews](https://www.kaggle.com/datasets)
- [Amazon Electronics Reviews](https://www.kaggle.com/datasets)
- [Datafiniti Amazon Reviews](https://www.kaggle.com/datasets)

---

## Configuration

All settings are in `app/config.py` and can be overridden via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `REVIEWS_CSV_PATH` | `data/reviews.csv` | Path to the reviews CSV |
| `TOP_N_ASPECTS` | `5` | Number of aspects to extract |
| `MIN_ASPECT_FREQ` | `2` | Minimum reviews an aspect must appear in |
| `MIN_REVIEWS` | `3` | Below this count → "not enough data" |
| `SUFFICIENT_REVIEWS` | `20` | Review count for confidence = 1.0 |

---

## Project Structure

```
app/
├── main.py              # FastAPI app + endpoints
├── models.py            # Pydantic schemas
├── config.py            # Central configuration
├── data_loader.py       # CSV loading + indexing
├── preprocessor.py      # Text cleaning + sentence splitting
├── aspect_extractor.py  # Noun-phrase extraction + noise filtering
├── sentiment_analyzer.py# VADER aspect sentiment
└── insights_engine.py   # Orchestrator (pros/cons/summary/confidence)
tests/
└── test_api.py          # Automated test suite
data/
└── reviews.csv          # Review dataset
```
