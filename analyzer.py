import requests
from bs4 import BeautifulSoup
import jieba
import pandas as pd
from datetime import datetime
from collections import defaultdict
import os

NEGATIVE_WORDS = ["爛", "死好", "氣死", "廢物", "崩潰", "糞", "無言", "討厭", "白爛", "垃圾", "不要臉", "爆氣"]
headers = {"cookie": "over18=1"}

def fetch_article_links(num_pages=10):
    base_url = "https://www.ptt.cc/bbs/Gossiping/index{}.html"
    pages_to_crawl = 10 
    board_url = f"{base_url}/bbs/Gossiping/index.html"
    links = []
    for _ in range(num_pages):
        res = requests.get(board_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        articles = soup.select("div.title a")
        for a in articles:
            links.append(base_url + a["href"])
        prev_page = soup.select_one("div.btn-group-paging a.btn.wide:nth-child(2)")
        if prev_page:
            board_url = base_url + prev_page["href"]
        else:
            break
    return links

def fetch_article_content(url):
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        time_str = soup.select_one("span.article-meta-tag:-soup-contains('時間')")
        time_value = time_str.find_next_sibling("span").text.strip()
        time_obj = datetime.strptime(time_value, "%a %b %d %H:%M:%S %Y")
        content = soup.select_one("#main-content").text.split("--\n")[0]
        return content, time_obj
    except:
        return "", None

def count_negative_words(text):
    words = jieba.lcut(text)
    return sum(1 for w in words if w in NEGATIVE_WORDS)

def analyze_trends():
    links = fetch_article_links(3)
    hour_trends = defaultdict(int)
    for url in links:
        content, time_obj = fetch_article_content(url)
        if not time_obj:
            continue
        hour_key = time_obj.strftime("%Y-%m-%d %H:00")
        count = count_negative_words(content)
        hour_trends[hour_key] += count
    df = pd.DataFrame(sorted(hour_trends.items()), columns=["hour", "negative_count"])
    if df.empty:
        return df
    base = df.iloc[0]["negative_count"]
    df["change_from_base"] = df["negative_count"] - base
    df["trend"] = df["change_from_base"].apply(lambda x: "↑" if x > 0 else ("↓" if x < 0 else "→"))
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/trends.csv", index=False)
    return df
