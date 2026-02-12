import streamlit as st
import pandas as pd
import yfinance as yf
from textblob import TextBlob
import plotly.express as px

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="FinAI Invest Bot",
    page_icon="📈",
    layout="wide"
)

# -------------------- SIDEBAR --------------------
st.sidebar.title("⚙️ Dashboard Controls")
ticker = st.sidebar.text_input("Enter Stock Ticker", "AAPL")
analyze_button = st.sidebar.button("🚀 Analyze")

st.sidebar.markdown("---")
st.sidebar.info("AI-Powered Financial Sentiment Dashboard")

# -------------------- MAIN TITLE --------------------
st.title("📈 FinAI Invest Bot")
st.markdown("### AI-Powered Market Sentiment & Investment Dashboard")

# -------------------- MAIN LOGIC --------------------
if analyze_button:

    with st.spinner("Fetching market data and analyzing sentiment..."):

        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="3mo")
            news = stock.news

            # -------------------- PRICE CHART --------------------
            if hist.empty:
                st.error("Invalid ticker or no market data found.")
                st.stop()

            st.subheader("📊 Stock Price (Last 3 Months)")
            fig_price = px.line(
                hist,
                x=hist.index,
                y="Close",
                title=f"{ticker.upper()} Price Trend",
            )
            st.plotly_chart(fig_price, use_container_width=True)

            # -------------------- NEWS SENTIMENT --------------------
            st.subheader("📰 News Sentiment Analysis")

            if not news:
                st.warning("No news found for this ticker.")
                st.stop()

            results = []
            scores = []

            for item in news[:10]:

                headline = None

                # Safe extraction
                if isinstance(item, dict):
                    headline = item.get("title")

                    # Some yfinance versions return nested structure
                    if headline is None and "content" in item:
                        content = item.get("content")
                        if isinstance(content, dict):
                            headline = content.get("title")

                if not headline:
                    continue

                sentiment_score = TextBlob(headline).sentiment.polarity
                scores.append(sentiment_score)

                if sentiment_score > 0.1:
                    signal = "BUY 📈"
                elif sentiment_score < -0.1:
                    signal = "SELL 📉"
                else:
                    signal = "HOLD ⚖️"

                results.append({
                    "Headline": headline,
                    "Sentiment Score": round(sentiment_score, 3),
                    "Signal": signal
                })

            if not results:
                st.warning("No valid news headlines available for sentiment analysis.")
                st.stop()

            df = pd.DataFrame(results)

            # -------------------- METRICS --------------------
            avg_sentiment = sum(scores) / len(scores)

            col1, col2 = st.columns(2)

            col1.metric("Average Sentiment Score", round(avg_sentiment, 3))

            if avg_sentiment > 0.1:
                overall_signal = "BUY 📈"
            elif avg_sentiment < -0.1:
                overall_signal = "SELL 📉"
            else:
                overall_signal = "HOLD ⚖️"

            col2.metric("Overall Investment Signal", overall_signal)

            # -------------------- SENTIMENT BAR CHART --------------------
            st.subheader("📊 Sentiment Distribution")

            fig_bar = px.bar(
                df,
                x="Headline",
                y="Sentiment Score",
                title="Sentiment per News Headline"
            )

            st.plotly_chart(fig_bar, use_container_width=True)

            # -------------------- DATA TABLE --------------------
            st.subheader("📋 Detailed Results")
            st.dataframe(df, use_container_width=True)

            # -------------------- DOWNLOAD BUTTON --------------------
            st.download_button(
                label="📥 Download CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name=f"{ticker}_sentiment.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"Unexpected error occurred: {e}")
