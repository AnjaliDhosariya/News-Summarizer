import streamlit as st
from services.news_fetcher import fetch_articles
from models.sentiments import analyze_sentiment
from models.tts import convert_text_to_speech
from config import RSS_FEEDS
from models.analysis import generate_final_sentiment_summary  # If implemented here
from models.analysis import compare_articles_with_ai  # If implemented here
import requests
from datetime import datetime


# Streamlit UI
st.set_page_config(page_title="News Summarizer", layout="wide")
st.title("📰 News Summarization & Sentiment Analysis App")

company_name = st.text_input("Enter Company Name", value="Google")

if st.button("Fetch News"):
    all_articles = []

    for source_name, url in RSS_FEEDS.items():
        articles = fetch_articles(source_name, url, company_name)
        all_articles.extend(articles)
        
    all_articles = sorted(all_articles, key=lambda x: x["published"], reverse=True)[:15]

    if all_articles:
        sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

        for article in all_articles:
            st.markdown(f"## 📰 {article['title']}")
            st.write(f"**📌 Publisher:** {article['publisher']}")
            st.write(f"🗓️ **Published Date:** {article['published'].strftime('%Y-%m-%d %H:%M:%S UTC')}")
            st.markdown(
                f"""<div style="font-family:Arial; font-size:16px; padding:10px; border-radius:5px;">
                <strong>Summary (English):</strong> {article['summary']}
                </div>""",
                unsafe_allow_html=True
            )
            st.audio(article["english_audio"])
            st.markdown(
                f"""<div style="font-family:Arial; font-size:16px; padding:10px; border-radius:5px;">
                <strong>Summary (Hindi):</strong> {article['summary_hindi']}
                </div>""",
                unsafe_allow_html=True
            )
            st.audio(article["hindi_audio"])

    # **Perform Sentiment Analysis Here**
            sentiment, sentiment_score = analyze_sentiment(article['summary'])
            sentiment_counts[sentiment] += 1
            final_sentiment = generate_final_sentiment_summary(all_articles, sentiment_counts)


            # **Display Sentiment AFTER the Summary**
            st.write(f"**📝 Sentiment Analysis:** {sentiment} ({sentiment_score})")
            
            st.markdown(f"[🔗 Read More]({article['link']})")
            st.markdown("---")
            
            # **Perform Comparative Analysis**
        comparison_results = compare_articles_with_ai(all_articles)

        # **Display Comparative Analysis in JSON Format**
        comparative_json = {
            "Comparative Sentiment Score": {
                "Sentiment Distribution": sentiment_counts,
                "Coverage Differences": comparison_results
            },
            "Final Sentiment Analysis": final_sentiment  # 🆕 Added final sentiment summary
        }

        st.subheader("📊 Comparative Sentiment Analysis")
        st.json(comparative_json)
    else:
        st.error(f"No relevant articles found for '{company_name}'.")


    

