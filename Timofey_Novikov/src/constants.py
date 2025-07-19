"""
Shared Constants Module
Centralized constants for sentiment analysis and configuration
"""

# Sentiment Analysis Keywords
SENTIMENT_KEYWORDS = {
    # Russian positive words
    'russian_positive': [
        'отлично', 'хорошо', 'прекрасно', 'удобно', 'нравится', 'люблю', 
        'классно', 'супер', 'замечательно', 'великолепно', 'благодарность', 
        'спасибо', 'лучший', 'интересно', 'полезно', 'рекомендую', 
        'расширил', 'возможность'
    ],
    
    # Russian negative words
    'russian_negative': [
        'плохо', 'ужасно', 'отстой', 'проблема', 'ошибка', 'баг', 'глюк', 
        'вылетает', 'тормозит', 'косячный', 'косяк', 'невозможно', 
        'отвратительно', 'кошмар', 'разочарован', 'жалоба', 'навязчиво', 
        'думайте', 'неделями', 'напоминать', 'впарит', 'претензией', 
        'отвечает', 'ответим'
    ],
    
    # English positive words
    'english_positive': [
        'good', 'great', 'excellent', 'amazing', 'love', 'like', 'best', 
        'awesome', 'fantastic', 'wonderful', 'perfect', 'brilliant', 
        'outstanding', 'superb', 'marvelous', 'incredible', 'fabulous', 'terrific'
    ],
    
    # English negative words
    'english_negative': [
        'bad', 'terrible', 'awful', 'horrible', 'hate', 'worst', 'crash', 
        'bug', 'problem', 'issue', 'slow', 'broken', 'useless', 'disappointing', 
        'frustrating', 'annoying', 'poor', 'fail'
    ]
}

# Feature Categories for Analysis
FEATURE_KEYWORDS = {
    'ui_design': ['interface', 'design', 'ui', 'ux', 'layout', 'look', 'appearance', 'visual'],
    'performance': ['speed', 'fast', 'slow', 'lag', 'performance', 'crash', 'freeze', 'bug'],
    'functionality': ['feature', 'function', 'work', 'working', 'functionality', 'capability'],
    'usability': ['easy', 'difficult', 'user-friendly', 'intuitive', 'simple', 'complex'],
    'support': ['support', 'help', 'customer', 'service', 'response', 'team'],
    'content': ['content', 'information', 'data', 'quality', 'accurate', 'updated']
}

# Issue Detection Keywords
ISSUE_KEYWORDS = [
    'crash', 'bug', 'error', 'problem', 'issue', 'broken', 'fail', 'wrong', 'bad'
]

# Configuration Defaults
DEFAULT_CONFIG = {
    'openai_model': 'gpt-4',
    'max_tokens': 1000,
    'temperature': 0.1,
    'max_retries': 3,
    'timeout': 30,
    'rate_limit_delay': 0.5,
    'max_reviews_per_batch': 15,
    'max_review_length': 10000
}

# Input Validation Limits
VALIDATION_LIMITS = {
    'min_review_length': 1,
    'max_review_length': 10000,
    'max_batch_size': 100,
    'allowed_chars_pattern': r'^[a-zA-Zа-яА-Я0-9\s\.\,\!\?\-\:\;\(\)\[\]\{\}\"\'\/\\\@\#\$\%\^\&\*\+\=\~\`\|<>👾🎯📊⭐💾🔍⚠️🎉]+$'
}

# Error Messages
ERROR_MESSAGES = {
    'openai_api_unavailable': 'OpenAI API is currently unavailable. Using fallback analysis.',
    'invalid_review_text': 'Review text contains invalid characters or is too long.',
    'empty_review': 'Review text is empty or too short.',
    'batch_too_large': f'Batch size exceeds maximum of {VALIDATION_LIMITS["max_batch_size"]} reviews.',
    'api_quota_exceeded': 'OpenAI API quota exceeded. Using keyword-based fallback analysis.'
}

# Logging Configuration
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file_max_bytes': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}