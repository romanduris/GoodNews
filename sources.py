# sources.py
import feedparser
import json
from datetime import datetime
from pathlib import Path

def load_sources(path="sources.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_feed(url, max_items=5):
    feed = feedparser.parse(url)
    articles = []
    for entry in getattr(feed, "entries", [])[:max_items]:
        articles.append({
            "title": getattr(entry, "title", ""),
            "link": getattr(entry, "link", ""),
            "summary": getattr(entry, "summary", ""),
            "published": getattr(entry, "published", ""),
            "source": url
        })
    return articles

def save_news(news):
    date_str = datetime.now().strftime("%Y-%m-%d")
    Path("data").mkdir(exist_ok=True)
    file_path = Path("data") / f"Sources.json"
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=2)
    print(f"✅ Uložené do {file_path}")

if __name__ == "__main__":
    sources = load_sources()
    all_news = []
    for s in sources:
        try:
            items = fetch_feed(s)
            if items:
                all_news.extend(items)
                print(f"✔ {s} -> {len(items)} položiek")
            else:
                print(f"⚠ Žiadne položky v: {s}")
        except Exception as e:
            print(f"ERR pri {s}: {e}")
    if all_news:
        save_news(all_news)
    else:
        print("Žiadne správy na uloženie.")
