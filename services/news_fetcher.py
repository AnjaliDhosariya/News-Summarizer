import requests
import feedparser
from newspaper import Article
from config import HEADERS, RSS_FEEDS
from utils import parse_date, get_publisher_name
from models.translator import translate_to_hindi
from models.tts import convert_text_to_speech
from models.sentiments import analyze_sentiment


def fetch_articles(feed_name, feed_url, company_name):
    """Fetch news articles from a given RSS feed."""
    articles_list = []
    response = requests.get(feed_url, headers=HEADERS)
    feed = feedparser.parse(response.content)

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        published = entry.get("published", "No Date")
        parsed_date = parse_date(published)
        summary = entry.get("summary", "")
        publisher = get_publisher_name(feed_name, link)

        if company_name.lower() in title.lower() or company_name.lower() in summary.lower():
            try:
                article = Article(link)
                article.download()
                article.parse()
                article.nlp()

                if company_name.lower() not in article.text.lower():
                    continue

                hindi_summary = translate_to_hindi(article.summary)
                english_audio = convert_text_to_speech(article.summary, lang="en")
                hindi_audio = convert_text_to_speech(hindi_summary, lang="hi")

                sentiment, sentiment_score = analyze_sentiment(article.summary)

                articles_list.append({
                    "title": title,
                    "publisher": publisher,
                    "published": parsed_date,
                    "summary": article.summary,
                    "summary_hindi": hindi_summary,
                    "link": link,
                    "english_audio": english_audio,
                    "hindi_audio": hindi_audio,
                    "sentiment": sentiment,
                    "sentiment_score": sentiment_score
                })

                if len(articles_list) >= 15:
                    break

            except Exception as e:
                print(f"Skipping article from {publisher} due to error: {e}")

    return articles_list
