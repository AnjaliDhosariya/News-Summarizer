import requests
from config import GROQ_API_KEY, GROQ_API_URL

def compare_articles_with_ai(articles):
    """Here using Groq API to perform comparative analysis on article titles."""
    if len(articles) < 2:
        return [{"Comparison": "Not enough articles for comparison.", "Impact": "Need at least 2 articles."}]

    titles = [f"{i+1}. {article['title']}" for i, article in enumerate(articles)]  # Numbered titles

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Compare the following news articles in terms of their focus, tone, and key takeaways:
    
    {titles}

    Return the analysis in this format:
    - **Comparison:** Clearly describe how two or more articles relate to each other using their actual titles.
    - **Impact:** Explain why these differences are important.

    Example Format:
    "Comparison: 'Google AI Breakthrough' focuses on innovation, while 'Google Faces Lawsuit' discusses legal issues."
    "Impact: This contrast highlights the company's dual challenges of advancing technology while handling legal concerns."

    Make sure to use **actual article titles** instead of vague labels like 'Article 1' and 'Article 2'.
    """

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "Analyze news coverage differences and their impact."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=10)

    if response.status_code == 200:
        analysis = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")

        if not analysis.strip():
            return [{"Comparison": "No insights generated.", "Impact": ""}]

        comparisons = []
        comparison = ""
        impact = ""

        analysis_lines = analysis.split("\n")

        for line in analysis_lines:
            if "Comparison:" in line:
                comparison = line.replace("Comparison:", "").strip()
            elif "Impact:" in line:
                impact = line.replace("Impact:", "").strip()
                comparisons.append({"Comparison": comparison, "Impact": impact})
                comparison = ""  # Reset for next comparison

        return comparisons if comparisons else [{"Comparison": "No insights generated.", "Impact": ""}]

    else:
        return [{"Comparison": f"Error: {response.status_code}", "Impact": "API failed to process request."}]


def generate_final_sentiment_summary(articles, sentiment_counts):
    """Useing Groq API to generate a final sentiment summary based on all articles."""
    if not articles:
        return "No sentiment analysis available."

    # Prepare data for AI
    titles = [f"{i+1}. {article['title']}" for i, article in enumerate(articles)]
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Analyze the sentiment of the following news articles:
    {titles}

    Sentiment Distribution:
    - Positive: {sentiment_counts["Positive"]}
    - Negative: {sentiment_counts["Negative"]}
    - Neutral: {sentiment_counts["Neutral"]}

    Based on this sentiment breakdown and the article topics, generate a **short summary** (max 2 sentences) of the overall sentiment.
    Example Output:
    "Tesla’s latest news coverage is mostly positive. Potential stock growth expected."

    Your summary:
    """

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "Analyze sentiment trends and generate a final summary."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=10)

    if response.status_code == 200:
        summary = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        return summary if summary else "No summary generated."
