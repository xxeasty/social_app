from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from textblob import TextBlob

import nltk
import os

nltk_data_dir = '/tmp/nltk_data'
nltk.download('punkt', download_dir=nltk_data_dir, quiet=True)
os.environ['NLTK_DATA'] = nltk_data_dir

nltk.download('vader_lexicon')

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """
    Analyze sentiment using VADER with score normalization.
    """
    scores = analyzer.polarity_scores(text)
    return (scores['compound'] + 1) * 5  # Normalize to 0-10 scale

def predict_personality(text):
    """
    Predict personality traits based on linguistic patterns in the user's text.
    """
    blob = TextBlob(text)
    word_count = len(blob.words)
    sentence_count = len(blob.sentences)
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
    sentiment_score = analyze_sentiment(text)

    # Heuristic-based personality predictions
    personality = {
        'openness': 0.5 + (avg_sentence_length / 20),  # Longer sentences may indicate openness
        'conscientiousness': 0.5 + (sentiment_score / 10),  # Positive sentiment may indicate conscientiousness
        'extraversion': 0.5 + (len([word for word in blob.words if word.lower() in ['i', 'we', 'us']]) / word_count),  # Use of personal pronouns
        'agreeableness': 0.5 + (sentiment_score / 10),  # Positive sentiment indicates agreeableness
        'neuroticism': 1 - (sentiment_score / 10),  # Negative sentiment indicates higher neuroticism
    }

    # Ensure values are between 0 and 1
    for trait in personality:
        personality[trait] = max(0, min(1, personality[trait]))

    return personality
