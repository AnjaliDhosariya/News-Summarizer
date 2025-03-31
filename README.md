# NewsInsight

## Overview
The **NewsInsight App** is a Streamlit-based web application that fetches the latest news articles related to a specific company, summarizes them, and performs sentiment analysis on the articles. It also provides comparative sentiment analysis and text-to-speech (TTS) functionality in both English and Hindi.

## Features
- **Fetch News Articles**: Retrieves news articles from multiple RSS feed sources based on a user-provided company name.
- **Summarization**: Generates a concise summary of each article in both English and Hindi.
- **Text-to-Speech (TTS)**: Converts the summarized text into audio (English & Hindi).
- **Sentiment Analysis**: Analyzes the sentiment of each article and classifies it as Positive, Negative, or Neutral.
- **Comparative Sentiment Analysis**: Evaluates sentiment distribution and coverage differences across sources.
- **User-Friendly Interface**: Interactive UI built with Streamlit.
- **Multi-Language Support**: Expand support to more languages beyond English and Hindi.
- **Customizable RSS Feeds**: Allow users to add or modify RSS feed sources dynamically.
- **Advanced Data Visualization**: Implement charts and graphs for better sentiment representation.

## Installation
### Prerequisites
Ensure you have Python 3 installed along with the necessary dependencies.

### Setup Instructions
1. **Clone the Repository**:
   ```sh
   git clone https://github.com/AnjaliDhosariya/NewsInsight.git
   cd news-summarization-app
   ```
2. **Create a Virtual Environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the Application**:
   ```sh
   streamlit run app.py
   ```

## Building the Application
To build and package the application for deployment:
1. **Ensure all dependencies are installed**:
   ```sh
   pip install -r requirements.txt
   ```
2. **Freeze dependencies**:
   ```sh
   pip freeze > requirements.txt
   ```
3. **Create an executable using PyInstaller (Optional for desktop app packaging)**:
   ```sh
   pyinstaller --onefile --name=news_app app.py
   ```
4. **Deploy on a Cloud Platform**:
   - Use **Streamlit Sharing**, **Heroku**, or **AWS Lambda** to deploy the app online.
   - Ensure that API keys and sensitive configurations are managed using environment variables.

## Configuration
- Update the `config.py` file with relevant RSS feed URLs under `RSS_FEEDS`.
- Ensure that `services/news_fetcher.py` and `models/` contain the necessary logic for fetching news, analyzing sentiment, and performing TTS.

## Usage
1. Open the web interface.
2. Enter a company name in the input field.
3. Click **Fetch News**.
4. View summarized news articles, listen to audio summaries, and analyze sentiment insights.

## Technologies Used
- **Translation**: Utilized **Grok API** for translating news summaries into Hindi.
- **Text-to-Speech (TTS)**: Used **gTTS (Google Text-to-Speech)** for converting text summaries into speech.
- **Summarization**: Implemented **NLTK (Natural Language Toolkit)** for generating concise article summaries.
- **News Extraction**: Employed **Feedparser** to extract news articles from RSS feeds.

## Future Improvements
- **Enhanced AI Analysis**: Improve sentiment analysis using advanced NLP models.
- **Real-time Updates**: Implement live news fetching rather than on-demand queries.
- **User Authentication**: Add a login system for personalized news tracking.
- **Mobile Compatibility**: Optimize UI for better mobile responsiveness.
- **Sentiment Trend Analysis**: Provide historical sentiment tracking over time.

## Dependencies
- `streamlit`
- `requests`
- `datetime`
- `feedparser`
- `nltk`
- `gtts`
- `services.news_fetcher`
- `models.sentiments`
- `models.tts`
- `models.analysis`

## Contributing
Feel free to submit pull requests or open issues to enhance the functionality of this project.

## License
This project is licensed under the MIT License.

## Acknowledgments
Thanks to the open-source community and the developers of the libraries used in this project.

