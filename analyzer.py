import pandas as pd
from datetime import datetime
import os

def analyze():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    neg_count = 3
    change = 1
    trend = "↑"

    new_row = pd.DataFrame([{
        "timestamp": now,
        "negative_count": neg_count,
        "change_from_base": change,
        "trend": trend
    }])

    if not os.path.exists("data"):
        os.makedirs("data")

    file_path = "data/trends.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df = new_row

    df.to_csv(file_path, index=False)

if __name__ == "__main__":
    analyze()
