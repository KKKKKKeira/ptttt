import os
import requests
import jieba
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
from datetime import datetime

NEGATIVE_WORDS = ["爛", "廢", "笨", "氣", "幹", "討厭", "垃圾", "死", "崩潰", "哭", "操", "怒", "噁", "醜", "爭議", "炎上"]

def fetch_articles():
    url = "https://www.ptt.cc/bbs/Gossiping/index.html"
    try:
        resp = requests.get(url, cookies={"over18": "1"}, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        links = soup.select("div.title a")
        articles = []
        for link in links[:10]:
            href = link["href"]
            article_url = f"https://www.ptt.cc{href}"
            article_resp = requests.get(article_url, cookies={"over18": "1"}, timeout=10)
            article_soup = BeautifulSoup(article_resp.text, "html.parser")
            content = article_soup.select_one("#main-content")
            if content:
                articles.append(content.get_text())
        return articles
    except Exception as e:
        print(f"Error fetching articles: {e}")
        return []

def analyze_trends():
    articles = fetch_articles()
    word_list = []
    for article in articles:
        words = jieba.lcut(article)
        word_list.extend(words)
    counter = Counter(word_list)
    neg_count = sum([counter[w] for w in NEGATIVE_WORDS])

    # 建立資料夾
    os.makedirs("data", exist_ok=True)

    # 記錄時間與變化量
    now = datetime.now().strftime("%Y-%m-%d %H:00")
    csv_path = "data/trends.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        base = df["negative_count"].iloc[0]
    else:
        base = neg_count
        df = pd.DataFrame(columns=["hour", "negative_count", "change_from_base", "trend"])

    change = neg_count - base
    trend = "→"
    if change > 0:
        trend = "↑"
    elif change < 0:
        trend = "↓"

    new_row = pd.DataFrame([{
        "hour": now,
        "negative_count": neg_count,
        "change_from_base": change,
        "trend": trend
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(csv_path, index=False)
    return df
