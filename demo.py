"""Demonstration script for Product Review Insights API."""
import httpx
import json

def test_product(pid, label):
    print(f"\n=== Testing {label} (ID: {pid}) ===")
    try:
        r = httpx.post("http://127.0.0.1:8000/api/v1/insights", json={"product_id": pid}, timeout=30.0)
        if r.status_code == 200:
            data = r.json()
            print(f"Status: {r.status_code}")
            print(f"Reviews Analyzed: {data['review_count']}")
            print(f"Confidence: {data['confidence']}")
            print(f"Summary: {data['summary']}")
            
            print("\nTop Aspects & Sentiment:")
            for a in data["top_aspects"]:
                print(f"  - {a['aspect']}: {a['sentiment']} (score: {a['score']})")
            
            print("\nPros (Sample):")
            for p in data["pros"][:2]:
                print(f"  [+] {p['point']}")
                print(f"      Evidence: \"{p['evidence']}\"")
                
            print("\nCons (Sample):")
            for c in data["cons"][:2]:
                print(f"  [-] {c['point']}")
                print(f"      Evidence: \"{c['evidence']}\"")
        else:
            print(f"Error {r.status_code}: {r.json()}")
    except Exception as e:
        print(f"Request failed: {e}")

# Product IDs from Datafiniti dataset
# AVqkIhwDv8e3D1O-lebb -> Fire HD 8 (High volume)
# AV-XeQLWuC1rwyj_gbP5 -> Fire TV (Small volume)
# NON_EXISTENT -> Testing 404

test_product("AVqkIhwDv8e3D1O-lebb", "Fire HD 8 Tablet")
test_product("AVqVGZNvQMlgsOJE6eUY", "Kindle Fire Tablet")
test_product("NON_EXISTENT", "Unknown Product (Edge Case)")
