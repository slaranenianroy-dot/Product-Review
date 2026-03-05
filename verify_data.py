import os
import pandas as pd
from app.data_loader import load_reviews
from app.config import settings

def verify_data():
    print(f"Checking for dataset at: {settings.DATA_PATH}")
    if not settings.DATA_PATH.exists():
        print(f"ERROR: Dataset file not found at {settings.DATA_PATH}.")
        return

    try:
        reviews = load_reviews()
        product_count = len(reviews)
        total_reviews = sum(len(rlist) for rlist in reviews.values())
        print(f"SUCCESS: Loaded {total_reviews} reviews for {product_count} products.")
        
        # Display some sample product IDs
        sample_ids = list(reviews.keys())[:5]
        print(f"Sample product IDs: {sample_ids}")
    except Exception as e:
        print(f"ERROR during data loading: {e}")

if __name__ == "__main__":
    verify_data()
