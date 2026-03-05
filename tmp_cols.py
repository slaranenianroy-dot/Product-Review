"""Quick CSV column viewer."""
import pandas as pd
import json

files = [
    r'c:\Hackathon\data\Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv',
    r'c:\Hackathon\data\1429_1.csv'
]

for f in files:
    print(f"--- {f} ---")
    df = pd.read_csv(f, nrows=1)
    print(", ".join(df.columns))
