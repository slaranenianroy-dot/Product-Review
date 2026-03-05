import pytest
import pandas as pd
import os
from app.data_loader import load_reviews, reset_cache
from app.config import settings

@pytest.fixture(autouse=True)
def clear_cache():
    reset_cache()
    yield
    reset_cache()

def test_load_reviews_success(tmp_path):
    """AC 2.1.1 & 2.1.2: Load CSV and index by product_id."""
    csv_file = tmp_path / "test_reviews.csv"
    df = pd.DataFrame({
        "product_id": ["P1", "P1", "P2"],
        "review_text": ["Good", "Better", "Bad"],
        "rating": [5, 4, 1],
        "review_date": ["2023-01-01", "2023-01-02", "2023-01-03"]
    })
    df.to_csv(csv_file, index=False)
    
    index = load_reviews(str(csv_file))
    
    assert len(index) == 2
    assert "P1" in index
    assert "P2" in index
    assert len(index["P1"]) == 2
    assert index["P1"][0]["review_text"] == "Good"

def test_load_reviews_missing_columns(tmp_path):
    """AC 2.1.3: Validate required columns."""
    csv_file = tmp_path / "malformed.csv"
    df = pd.DataFrame({
        "product_id": ["P1"],
        "review_text": ["Good"]
        # Missing rating and review_date
    })
    df.to_csv(csv_file, index=False)
    
    with pytest.raises(ValueError, match="missing required columns"):
        load_reviews(str(csv_file))

def test_load_reviews_empty_text(tmp_path):
    """AC 2.1.4: Drop rows with empty review_text."""
    csv_file = tmp_path / "empty_text.csv"
    df = pd.DataFrame({
        "product_id": ["P1", "P2"],
        "review_text": ["Good", ""],  # P2 has empty text
        "rating": [5, 4],
        "review_date": ["2023-01-01", "2023-01-02"]
    })
    df.to_csv(csv_file, index=False)
    
    index = load_reviews(str(csv_file))
    
    assert "P1" in index
    assert "P2" not in index
    assert len(index) == 1

def test_load_reviews_file_not_found():
    """AC 2.1.5: Raise FileNotFoundError if missing."""
    with pytest.raises(FileNotFoundError):
        load_reviews("non_existent_file.csv")
