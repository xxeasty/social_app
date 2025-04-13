from kiwipiepy import Kiwi
import numpy as np

# Initialize Kiwi
kiwi = Kiwi()

# Korean sentiment lexicon (customizable)
SENTIMENT_LEXICON = {
    '좋다': 2, '기쁘다': 2, '행복': 3, '사랑': 3,  # Positive
    '나쁘다': -2, '슬프다': -3, '화나다': -3, '미워': -3  # Negative
}

def analyze_sentiment(text):
    """Korean sentiment analysis without Java"""
    tokens = kiwi.tokenize(text)
    score = sum(SENTIMENT_LEXICON.get(token[0], 0) for token in tokens)  # Use index [0] for token text
    return max(0, min(10, (score + 10) * 0.5))  # Scale to 0-10

def predict_personality(text):
    """Personality prediction using Korean linguistic patterns"""
    analysis = kiwi.analyze(text)
    
    # Handle empty analysis
    if not analysis or not analysis[0][0]:
        return default_personality()
    
    # Extract tokens from first analysis result
    tokens = analysis[0][0]  # (tokens, score, position)
    pos_tags = [(token[0], token[1]) for token in tokens]  # Use index access
    
    # Feature extraction
    noun_count = sum(1 for _, tag in pos_tags if tag.startswith('NN'))
    verb_count = sum(1 for _, tag in pos_tags if tag.startswith('VV'))
    adj_count = sum(1 for _, tag in pos_tags if tag.startswith('VA'))
    sentence_len = len(text.strip()) / 100
    
    # Personality calculations
    return {
        'openness': np.clip(0.4 + noun_count/15 + adj_count/10, 0, 1),
        'conscientiousness': np.clip(0.5 + verb_count/12 - sentence_len/5, 0, 1),
        'extraversion': np.clip(0.5 + (noun_count + verb_count)/20, 0, 1),
        'agreeableness': np.clip(0.6 + analyze_sentiment(text)/15, 0, 1),
        'neuroticism': np.clip(0.4 - analyze_sentiment(text)/20, 0, 1)
    }

def default_personality():
    """Fallback personality profile"""
    return {
        'openness': 0.5,
        'conscientiousness': 0.5,
        'extraversion': 0.5,
        'agreeableness': 0.5,
        'neuroticism': 0.5
    }