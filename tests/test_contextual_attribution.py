import pytest
from app.sentiment_analyzer import analyze_aspect_sentiment
from app.config import settings

def test_negative_aspect_in_5_star_review():
    """
    Story 3.3.1: 5-star review with a 'buried' negative.
    The overall rating is high, but the text contains a specific complaint.
    """
    reviews = [
        {
            "rating": 5.0,
            "sentences": ["I love this phone.", "However, the battery life is terrible."],
            "review_text": "I love this phone. However, the battery life is terrible."
        }
    ]
    
    # Analyze 'battery'
    # It should be negative because the clause 'battery life is terrible' is negative.
    info = analyze_aspect_sentiment(reviews, "battery life")
    assert info["sentiment"] == "negative"
    assert info["score"] < 0

def test_mixed_rating_attribution():
    """
    Ensure aspects from different reviews don't bleed together incorrectly 
    and maintain their source-level sentiment.
    """
    reviews = [
        {
            "rating": 5.0,
            "sentences": ["Great screen."],
            "review_text": "Great screen."
        },
        {
            "rating": 1.0,
            "sentences": ["Horrible screen."],
            "review_text": "Horrible screen."
        }
    ]
    
    # 'screen' should be neutral (average of + and -) or mixed.
    # Our current logic averages them.
    info = analyze_aspect_sentiment(reviews, "screen")
    # VADER 'great' vs 'horrible' usually yields a score near 0 if averaged.
    # Let's check the behavior.
    assert len(info["sentence_scores"]) == 2
    # In VADER: 'Great screen' ~ 0.62, 'Horrible screen' ~ -0.54. Average ~ 0.04.
    # settings.POSITIVE_THRESHOLD is 0.05, settings.NEGATIVE_THRESHOLD is -0.05.
    # So it might be 'neutral'.
    assert info["sentiment"] == "neutral"

def test_conjunction_but_attribution():
    """5-star review: 'Love it but the cable is flimsy'."""
    reviews = [
        {
            "rating": 5.0,
            "sentences": ["Love the camera, but the cable is flimsy."],
            "review_text": "Love the camera, but the cable is flimsy."
        }
    ]
    
    # 'cable' should be negative
    cable_info = analyze_aspect_sentiment(reviews, "cable")
    assert cable_info["sentiment"] == "negative"
    assert cable_info["score"] < 0
    
    # 'camera' should be positive
    camera_info = analyze_aspect_sentiment(reviews, "camera")
    assert camera_info["sentiment"] == "positive"
    assert camera_info["score"] > 0
