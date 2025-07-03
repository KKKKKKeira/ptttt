import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_plot(csv_path="data/trends.csv", output_path="static/trend_plot.png"):
    if not os.path.exists(csv_path):
        return False
    df = pd.read_csv(csv_path)
    if df.empty:
        return False
    plt.figure(figsize=(10, 5))
    plt.plot(df["hour"], df["change_from_base"], marker='o', linestyle='-', color='red')
    plt.xticks(rotation=45)
    plt.title("PTT 八卦版情緒趨勢圖")
    plt.xlabel("時間")
    plt.ylabel("變化量（相對基準）")
    plt.tight_layout()
    os.makedirs("static", exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    return True
