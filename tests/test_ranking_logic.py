import pytest
from app.insights_engine import generate_insights
from app.config import settings

def test_ranking_frequency_vs_strength():
    """
    Story 3.4.1 & 3.4.5: High frequency should outrank low frequency if impact is higher.
    Aspect A: 5 mentions, sentiment 0.2 -> Impact 1.0
    Aspect B: 1 mention, sentiment 0.9 -> Impact 0.9
    Result: A should be first.
    """
    reviews = []
    # Aspect A: 'screen' (5 positive mentions)
    for _ in range(5):
        reviews.append({
            "product_id": "P1",
            "rating": 5.0,
            "review_text": "The screen is good.",
            "sentences": ["The screen is good."]
        })
    
    # Aspect B: 'battery' (1 very positive mention)
    reviews.append({
        "product_id": "P1",
        "rating": 5.0,
        "review_text": "The battery is absolutely perfect and amazing!",
        "sentences": ["The battery is absolutely perfect and amazing!"]
    })

    # We need to make sure both are extracted. 
    # 'screen' frequency = 5, 'battery' frequency = 1.
    # Note: MIN_ASPECT_FREQUENCY is 2 by default. 
    # Let's add one more battery mention to ensure extraction.
    reviews.append({
        "product_id": "P1",
        "rating": 5.0,
        "review_text": "The battery is okay.",
        "sentences": ["The battery is okay."]
    })
    # Now battery frequency = 2.
    # Let's adjust Aspect A to 5 mentions.
    
    result = generate_insights("P1", reviews)
    
    top_aspects = result["top_aspects"]
    # Verify screen is #1 and battery is #2
    # Screen impact: 5 * 0.44 (approx for 'good') = 2.2
    # Battery impact: (1 * 0.9 + 1 * 0.2) / 2 = 0.55 avg * 2 freq = 1.1
    
    assert top_aspects[0]["aspect"] == "screen"
    assert top_aspects[1]["aspect"] == "battery"

def test_pros_cons_sorting():
    """Verify pros and cons are individually sorted by impact."""
    reviews = []
    # Pro 1: 'audio' (High impact: 5 reviews * strong)
    for _ in range(5):
        reviews.append({"product_id": "P2", "rating": 5.0, "review_text": "The audio is excellent.", "sentences": ["The audio is excellent."]})
    # Pro 2: 'battery' (Low impact: 2 reviews * weak)
    for _ in range(2):
        reviews.append({"product_id": "P2", "rating": 5.0, "review_text": "The battery is fine.", "sentences": ["The battery is fine."]})
    
    # Con 1: 'heat' (High impact)
    for _ in range(5):
        reviews.append({"product_id": "P2", "rating": 1.0, "review_text": "The heat is terrible.", "sentences": ["The heat is terrible."]})
    # Con 2: 'sound' (Low impact)
    for _ in range(2):
        reviews.append({"product_id": "P2", "rating": 1.0, "review_text": "The sound is poor.", "sentences": ["The sound is poor."]})
    
    result = generate_insights("P2", reviews)
    # Assert sorting in pros: audio should be first
    assert "audio" in result["pros"][0]["point"].lower()
    assert "battery" in result["pros"][1]["point"].lower()
    
    # Assert sorting in cons: heat should be first
    assert "heat" in result["cons"][0]["point"].lower()
    assert "sound" in result["cons"][1]["point"].lower()

def test_top_n_limit():
    """Verify output lists are limited to TOP_N_ASPECTS."""
    reviews = []
    # Use real words that are likely to be noun chunks
    aspects = ["screen", "battery", "camera", "sound", "price", "size", "color"]
    for i, aspect in enumerate(aspects):
        # Higher index = lower impact
        count = 10 - i
        for _ in range(count):
            reviews.append({
                "product_id": "P3",
                "rating": 5.0,
                "review_text": f"The {aspect} is perfect.",
                "sentences": [f"The {aspect} is perfect."]
            })
            
    result = generate_insights("P3", reviews, top_n=3)
    
    assert len(result["top_aspects"]) == 3
    assert len(result["pros"]) == 3
    assert result["top_aspects"][0]["aspect"] == "screen"
    assert result["top_aspects"][2]["aspect"] == "camera"
