from transformers import pipeline

# Load DistilBERT-based sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", framework="pt")

def analyze_sentiment(text):
    try:
        print(f"[Sentiment Analysis] Analyzing sentiment for text: {text}")
        sentiment_results = sentiment_analyzer(text)
        sentiment_label = sentiment_results[0].get('label', 'neutral').lower()
        sentiment_score = sentiment_results[0].get('score', 0.0)

        sentiment_mapping = {
            "positive": "positive",
            "negative": "negative",
            "neutral": "neutral"
        }

        sentiment = sentiment_mapping.get(sentiment_label, "neutral")
        print(f"[Sentiment Analysis] Analysis result: {sentiment}, Score: {sentiment_score}")
        return sentiment, sentiment_score
    except Exception as e:
        print(f"[Sentiment Analysis] Error during analysis: {str(e)}")
        return "N/A", "N/A"
