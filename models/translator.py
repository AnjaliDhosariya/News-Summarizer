import requests
from config import GROQ_API_KEY, GROQ_API_URL
import time

def translate_to_hindi(text):
    """This function sends English text to Groq API and translates it to Hindi."""
    if not text.strip():
        return "Translation Failed: Empty Text"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    cleaned_text = text.replace("£", "GBP").replace("€", "EUR").replace("$", "USD")

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "Translate the following English text into Hindi."},
            {"role": "user", "content": cleaned_text}
        ],
        "temperature": 0.7
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=10)

            if response.status_code == 200:
                response_json = response.json()
                translation = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
                return translation.replace("\n", " ") if translation else "Translation Failed: Empty API Response"

            elif response.status_code == 401:
                return "Translation Error: Invalid API Key"

            elif response.status_code == 429:
                print("Rate Limit Exceeded. Retrying after 10 seconds...")
                time.sleep(10)
            else:
                print(f"API Error: {response.status_code} - {response.text}")

        except requests.exceptions.Timeout:
            print("Request Timed Out. Retrying...")
            time.sleep(5)

        except requests.exceptions.RequestException as e:
            print(f"API Request Failed: {e}")
            return "Translation Error: Network Issue"

    return "Translation Error: Could Not Complete Request"
