from fastapi import FastAPI, Query
from typing import Dict, List
from services.news_fetcher import fetch_articles
from models.sentiments import analyze_sentiment
from models.tts import convert_text_to_speech
from models.translator import translate_to_hindi
from models.analysis import compare_articles_with_ai, generate_final_sentiment_summary
from config import RSS_FEEDS

app = FastAPI(title="News Summarization API", description="API for fetching news, performing sentiment analysis, and TTS")

@app.get("/")
def home():
    return {"message": "Welcome to the News Summarization API"}

@app.get("/fetch-news/")
def get_news(company_name: str = Query(..., description="Company name to fetch news for")):
    """Fetch news articles related to a company"""
    all_articles = []

    for source_name, url in RSS_FEEDS.items():
        articles = fetch_articles(source_name, url, company_name)
        all_articles.extend(articles)

    all_articles = sorted(all_articles, key=lambda x: x["published"], reverse=True)[:15]

    if not all_articles:
        return {"error": f"No relevant articles found for '{company_name}'"}

    return {"company": company_name, "articles": all_articles}

@app.post("/analyze-sentiment/")
def sentiment_analysis(article_text: str):
    """Perform sentiment analysis on a given text"""
    sentiment, score = analyze_sentiment(article_text)
    return {"sentiment": sentiment, "score": score}

@app.post("/translate/")
def translate_text(text: str):
    """Translate English text to Hindi"""
    hindi_translation = translate_to_hindi(text)
    return {"original_text": text, "translated_text": hindi_translation}

@app.post("/text-to-speech/")
def text_to_speech(text: str, lang: str = "en"):
    """Convert text to speech"""
    audio_path = convert_text_to_speech(text, lang)
    if not audio_path:
        return {"error": "Failed to generate speech"}
    return {"audio_file": audio_path}

@app.post("/compare-articles/")
def compare_articles(articles: List[Dict]):
    """Compare multiple articles for key takeaways"""
    comparison_results = compare_articles_with_ai(articles)
    return {"comparative_analysis": comparison_results}

@app.post("/final-sentiment/")
def final_sentiment_summary(articles: List[Dict]):
    """Generate a final sentiment summary for multiple articles"""
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for article in articles:
        sentiment_counts[article["sentiment"]] += 1

    final_summary = generate_final_sentiment_summary(articles, sentiment_counts)
    return {"final_sentiment_summary": final_summary}

