# sentiment.py
import json
from textblob import TextBlob
from pathlib import Path

def analyze_sentiment(text):
    """Vypočíta polarity TextBlob (-1 až +1)"""
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def process_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        articles = json.load(f)

    # Krok 1: spočítaj polaritu pre každý článok
    for article in articles:
        text = article.get("title", "") + " " + article.get("summary", "")
        article["raw_polarity"] = analyze_sentiment(text)

    # Krok 2: nájdeme max a min polaritu v datasetu
    polarities = [a["raw_polarity"] for a in articles]
    max_p = max(polarities) if polarities else 1
    min_p = min(polarities) if polarities else -1

    range_p = max_p - min_p if max_p != min_p else 1  # zabránime deleniu nulou

    # Krok 3: normalizácia do 0-100 % podľa relatívnej pozitivity
    for article in articles:
        article["sentiment_percent"] = int((article["raw_polarity"] - min_p) / range_p * 100)

    # Krok 4: zorad od najpozitívnejších po najnegatívnejšie
    articles.sort(key=lambda x: x["sentiment_percent"], reverse=True)

    # uložíme do JSON
    Path(output_file).parent.mkdir(exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"✅ Sentiment analyzovaný a uložený do {output_file}")

if __name__ == "__main__":
    process_file("data/news_2025-10-22-14-37.json", "data/news_sentiment.json")
