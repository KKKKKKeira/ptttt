
import requests
from bs4 import BeautifulSoup
import jieba
import pandas as pd
from collections import Counter
from datetime import datetime
import re
import os

# 更強的負面詞庫
NEGATIVE_WORDS = [
    "爛", "垃圾", "噁心", "崩潰", "不爽", "無言", "生氣",
    "痛苦", "難過", "不合理", "爆氣", "離譜", "討厭",
    "低能", "1450", "塔綠班", "支那", "死好", "腦殘", "豬隊友"
]

def crawl_ptt_articles(pages=10):
    session = requests.Session()
    session.cookies.set("over18", "1")
    articles = []

    base_url = "https://www.ptt.cc/bbs/Gossiping/index{}.html"
    for i in range(1, pages + 1):
        url = base_url.format(i)
        r = session.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        entries = soup.select(".r-ent")
        for entry in entries:
            href = entry.select_one("a")
            if href:
                article_url = "https://www.ptt.cc" + href["href"]
                try:
                    ar = session.get(article_url)
                    ar.encoding = "utf-8"
                    soup = BeautifulSoup(ar.text, "html.parser")
                    main_content = soup.select_one("#main-content")
                    if main_content:
                        text = main_content.get_text()
                        text = re.sub(r"(※|◆|--|編輯|發信站).*", "", text)
                        articles.append({
                            "url": article_url,
                            "content": text
                        })
                except:
                    continue
    return articles

def analyze_trends():
    articles = crawl_ptt_articles()
    trend_data = []

    for article in articles:
        content = article["content"]
        words = jieba.lcut(content)
        hour = datetime.now().replace(minute=0, second=0, microsecond=0)
        negative_count = sum(1 for w in words if w in NEGATIVE_WORDS)
        trend_data.append({"hour": hour, "negative_count": negative_count})

    # 聚合每小時
    df = pd.DataFrame(trend_data)
    if df.empty:
        return pd.DataFrame()
    df = df.groupby("hour").sum().reset_index()
    df["hour"] = df["hour"].astype(str)

    base = df["negative_count"].iloc[0]
    df["change_from_base"] = df["negative_count"] - base
    df["trend"] = df["change_from_base"].apply(
        lambda x: "↑" if x > 0 else ("↓" if x < 0 else "→")
    )

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/trends.csv", index=False)
    return df
