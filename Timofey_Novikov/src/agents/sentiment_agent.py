"""
Simple Sentiment Analysis Agent
Mock implementation for TDD
"""

from typing import Dict, Any


class SentimentAgent:
    """Mock sentiment analysis agent"""
    
    def __init__(self):
        """Initialize sentiment agent"""
        self.model = "gpt-4.1"
        self.temperature = 0.1
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text using basic keyword analysis
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment analysis results
        """
        
        # Basic sentiment analysis using keywords
        text_lower = text.lower()
        
        # Import shared sentiment keywords
        from ..constants import SENTIMENT_KEYWORDS
        
        positive_words = (SENTIMENT_KEYWORDS['english_positive'] + 
                         SENTIMENT_KEYWORDS['russian_positive'])
        
        negative_words = (SENTIMENT_KEYWORDS['english_negative'] + 
                         SENTIMENT_KEYWORDS['russian_negative'])
        
        # Count sentiment words
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        # Determine sentiment
        if positive_count > negative_count:
            sentiment = 'POSITIVE'
            confidence = min(0.9, 0.6 + (positive_count * 0.1))
            emotions = ['joy', 'satisfaction']
            intensity = 'high' if positive_count > 2 else 'medium'
        elif negative_count > positive_count:
            sentiment = 'NEGATIVE'
            confidence = min(0.9, 0.6 + (negative_count * 0.1))
            emotions = ['frustration', 'disappointment']
            intensity = 'high' if negative_count > 2 else 'medium'
        else:
            sentiment = 'NEUTRAL'
            confidence = 0.5
            emotions = ['neutral']
            intensity = 'low'
        
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'emotions': emotions, 
            'intensity': intensity,
            'positive_words_found': positive_count,
            'negative_words_found': negative_count
        }