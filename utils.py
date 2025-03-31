# utils.py
import nltk
from datetime import datetime, timezone
import dateutil.parser
from urllib.parse import urlparse

def get_publisher_name(feed_name, entry_link):
    """Extracts the publisher name based on the RSS source or URL."""
    if "BBC" in feed_name:
        return "BBC News"
    elif "Moneycontrol" in feed_name:
        return "Moneycontrol"
    elif "NYTimes" in feed_name:
        return "New York Times"
    elif "CNN" in feed_name:
        return "CNN"
    elif "The Guardian" in feed_name:
        return "The Guardian"
    
    parsed_url = urlparse(entry_link)
    return parsed_url.netloc.replace("www.", "")

def parse_date(published):
    """Parses the published date string into a datetime object."""
    try:
        return dateutil.parser.parse(published).replace(tzinfo=timezone.utc)
    except Exception:
        return datetime.now(timezone.utc)
