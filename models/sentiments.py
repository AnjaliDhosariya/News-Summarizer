import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download("vader_lexicon")
import requests
from config import GROQ_API_KEY, GROQ_API_URL

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """Performing sentiment analysis on the summary using VADER."""
    sentiment_scores = sia.polarity_scores(text)
    compound_score = sentiment_scores["compound"]
    
    if compound_score >= 0.05:
        sentiment = "Positive"
    elif compound_score <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    return sentiment, round(compound_score, 3)

