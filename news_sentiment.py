# news_sentiment.py
# Real Financial News Sentiment → Investment Signals → CSV Export

import csv
import os
import feedparser


# 1️⃣ Load real financial news from Yahoo Finance
def load_real_news():
    rss_url = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=market&region=US&lang=en-US"
    feed = feedparser.parse(rss_url)

    headlines = []
    for entry in feed.entries[:5]:
        headlines.append(entry.title)

    return headlines


# 2️⃣ Simple sentiment analysis logic
def analyze_sentiment(headline):
    positive_words = [
        "rally", "strong", "optimistic", "growth",
        "cooling", "earnings", "gain", "rise"
    ]
    negative_words = [
        "fall", "decline", "recession", "fears",
        "tensions", "loss", "drop", "crash"
    ]

    score = 0
    text = headline.lower()

    for word in positive_words:
        if word in text:
            score += 1

    for word in negative_words:
        if word in text:
            score -= 1

    if score > 0:
        return score, "Positive"
    elif score < 0:
        return score, "Negative"
    else:
        return score, "Neutral"


# 3️⃣ Convert sentiment into investment signal
def investment_signal(sentiment):
    if sentiment == "Positive":
        return "BUY"
    elif sentiment == "Negative":
        return "SELL"
    else:
        return "HOLD"


# 4️⃣ Save analysis results to CSV
def save_to_csv(results):
    os.makedirs("../outputs", exist_ok=True)
    file_path = "../outputs/investment_insights.csv"

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "News Headline",
            "Sentiment",
            "Sentiment Score",
            "Investment Signal"
        ])

        for row in results:
            writer.writerow(row)

    print(f"\n✅ Results saved to: {file_path}")


# 5️⃣ Main execution flow
def main():
    news = load_real_news()
    results = []

    print("\n📊 AI-Driven Market Sentiment & Investment Signals\n")

    for headline in news:
        score, sentiment = analyze_sentiment(headline)
        signal = investment_signal(sentiment)

        print(f"📰 {headline}")
        print(f"Sentiment: {sentiment} | Score: {score}")
        print(f"Investment Signal: {signal}\n")

        results.append([headline, sentiment, score, signal])

    save_to_csv(results)


# 6️⃣ Run program
if __name__ == "__main__":
    main()
