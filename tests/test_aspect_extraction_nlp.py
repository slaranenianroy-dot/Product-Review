import pytest
from app.aspect_extractor import extract_aspects
from app.config import settings

def test_extract_basic_aspects():
    """Verify that common nouns are extracted as aspects."""
    reviews = [
        {
            "sentences": ["The battery life is amazing.", "I love the screen quality."],
            "review_text": "The battery life is amazing. I love the screen quality."
        },
        {
            "sentences": ["Great battery and fast charging."],
            "review_text": "Great battery and fast charging."
        }
    ]
    
    # We need to lower the MIN_ASPECT_FREQUENCY for testing if needed
    # but here 2 reviews both mention battery (one as 'battery life' head 'battery', one as 'battery')
    
    aspects = extract_aspects(reviews, top_n=5)
    aspect_names = [a["aspect"] for a in aspects]
    
    assert "battery" in aspect_names
    # 'screen' or 'quality' should be there too if frequency allows
    # In this mock, screen only appears once.

def test_extract_noun_chunks():
    """Verify that multi-word aspects (noun chunks) are captured."""
    reviews = [
        {"sentences": ["The sound quality is crisp."], "review_text": "The sound quality is crisp."},
        {"sentences": ["Amazing sound quality and bass."], "review_text": "Amazing sound quality and bass."}
    ]
    
    aspects = extract_aspects(reviews, top_n=5)
    aspect_names = [a["aspect"] for a in aspects]
    
    # 'sound quality' (full chunk) and 'quality' (head) should be candidates
    assert any("sound quality" in name for name in aspect_names) or "quality" in aspect_names

def test_lemmatization():
    """Verify that plural/singular aspects are grouped."""
    reviews = [
        {"sentences": ["The button is loose."], "review_text": "The button is loose."},
        {"sentences": ["These buttons feel cheap."], "review_text": "These buttons feel cheap."}
    ]
    
    aspects = extract_aspects(reviews, top_n=5)
    aspect_names = [a["aspect"] for a in aspects]
    
    # Both should lemma to 'button'
    assert "button" in aspect_names

def test_filtering_logic():
    """Verify that stopwords and short words are filtered."""
    reviews = [
        {"sentences": ["It is a very big it."], "review_text": "It is a very big it."},
        {"sentences": ["It is just an it."], "review_text": "It is just an it."}
    ]
    
    aspects = extract_aspects(reviews, top_n=5)
    # 'it' is a stopword or too short (< 3 usually)
    for a in aspects:
        assert a["aspect"] != "it"
