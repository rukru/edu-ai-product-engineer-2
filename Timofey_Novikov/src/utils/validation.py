"""
Input Validation and Sanitization Module
Ensures safe and valid input for all analysis functions
"""

import re
import html
import logging
from typing import List, Dict, Any, Tuple, Optional
from ..constants import VALIDATION_LIMITS, ERROR_MESSAGES

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class InputValidator:
    """Handles input validation and sanitization"""
    
    def __init__(self):
        self.char_pattern = re.compile(VALIDATION_LIMITS['allowed_chars_pattern'])
        self.min_length = VALIDATION_LIMITS['min_review_length']
        self.max_length = VALIDATION_LIMITS['max_review_length']
        self.max_batch_size = VALIDATION_LIMITS['max_batch_size']
    
    def sanitize_text(self, text: str) -> str:
        """Sanitize text input by removing/escaping harmful content"""
        if not isinstance(text, str):
            text = str(text)
        
        # HTML escape to prevent injection
        text = html.escape(text)
        
        # Remove null bytes and control characters (except newlines, tabs)
        text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Limit length to prevent memory issues
        if len(text) > self.max_length:
            text = text[:self.max_length]
            logger.warning(f"Text truncated to {self.max_length} characters")
        
        return text
    
    def validate_review_text(self, text: str) -> Tuple[bool, str]:
        """
        Validate a single review text
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not text or not isinstance(text, str):
            return False, ERROR_MESSAGES['empty_review']
        
        # Sanitize first
        clean_text = self.sanitize_text(text)
        
        # Check length
        if len(clean_text) < self.min_length:
            return False, ERROR_MESSAGES['empty_review']
        
        if len(clean_text) > self.max_length:
            return False, ERROR_MESSAGES['invalid_review_text']
        
        # Check for valid characters (allow emojis and international chars)
        # More permissive check - just ensure no dangerous characters
        dangerous_patterns = [
            r'<script',  # Script tags
            r'javascript:',  # Javascript URLs  
            r'data:text/html',  # Data URLs
            r'vbscript:',  # VBScript
            r'on\w+\s*=',  # Event handlers
        ]
        
        text_lower = clean_text.lower()
        for pattern in dangerous_patterns:
            if re.search(pattern, text_lower):
                return False, ERROR_MESSAGES['invalid_review_text']
        
        return True, ""
    
    def validate_review_batch(self, reviews: List[str]) -> Tuple[bool, str, List[str]]:
        """
        Validate a batch of reviews
        
        Returns:
            Tuple of (is_valid, error_message, cleaned_reviews)
        """
        if not reviews or not isinstance(reviews, list):
            return False, ERROR_MESSAGES['empty_review'], []
        
        if len(reviews) > self.max_batch_size:
            return False, ERROR_MESSAGES['batch_too_large'], []
        
        cleaned_reviews = []
        invalid_count = 0
        
        for i, review in enumerate(reviews):
            is_valid, error_msg = self.validate_review_text(review)
            
            if is_valid:
                cleaned_reviews.append(self.sanitize_text(review))
            else:
                invalid_count += 1
                logger.warning(f"Review {i+1} invalid: {error_msg}")
        
        if not cleaned_reviews:
            return False, "No valid reviews found in batch", []
        
        if invalid_count > 0:
            logger.info(f"Removed {invalid_count} invalid reviews from batch")
        
        return True, "", cleaned_reviews
    
    def validate_analysis_params(self, params: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate analysis parameters
        
        Args:
            params: Dictionary of analysis parameters
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        valid_params = {
            'parallel': bool,
            'timeout': (int, float),
            'max_retries': int,
            'temperature': (int, float),
            'max_tokens': int
        }
        
        for key, value in params.items():
            if key in valid_params:
                expected_type = valid_params[key]
                if not isinstance(value, expected_type):
                    return False, f"Parameter '{key}' must be of type {expected_type.__name__}"
                
                # Range validations
                if key == 'temperature' and not 0 <= value <= 2:
                    return False, "Temperature must be between 0 and 2"
                
                if key == 'max_tokens' and not 1 <= value <= 8000:
                    return False, "Max tokens must be between 1 and 8000"
                
                if key == 'max_retries' and not 0 <= value <= 10:
                    return False, "Max retries must be between 0 and 10"
                
                if key == 'timeout' and not 1 <= value <= 300:
                    return False, "Timeout must be between 1 and 300 seconds"
        
        return True, ""
    
    def safe_extract_text(self, data: Any, max_depth: int = 3) -> str:
        """
        Safely extract text from various data types
        
        Args:
            data: Input data (str, dict, list, etc.)
            max_depth: Maximum recursion depth for nested structures
            
        Returns:
            Cleaned text string
        """
        if max_depth <= 0:
            return ""
        
        if isinstance(data, str):
            return self.sanitize_text(data)
        
        elif isinstance(data, dict):
            # Extract text from common text fields
            text_fields = ['content', 'text', 'message', 'review', 'comment', 'body']
            for field in text_fields:
                if field in data:
                    return self.safe_extract_text(data[field], max_depth - 1)
            
            # Fallback: concatenate all string values
            texts = []
            for value in data.values():
                if isinstance(value, str):
                    texts.append(self.safe_extract_text(value, max_depth - 1))
            
            return " ".join(texts)
        
        elif isinstance(data, list):
            texts = []
            for item in data[:10]:  # Limit to first 10 items
                text = self.safe_extract_text(item, max_depth - 1)
                if text:
                    texts.append(text)
            
            return " ".join(texts)
        
        else:
            # Convert to string and sanitize
            return self.sanitize_text(str(data))
    
    def validate_api_response(self, response: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate API response structure
        
        Args:
            response: API response dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(response, dict):
            return False, "Response must be a dictionary"
        
        # Check for error indicators
        if 'error' in response:
            error_msg = response.get('error', 'Unknown error')
            # Sanitize error message to prevent log injection
            safe_error = self.sanitize_text(str(error_msg))
            return False, f"API error: {safe_error[:200]}"
        
        # Check for required fields in successful responses
        required_fields = ['sentiment', 'processing_time']
        missing_fields = [field for field in required_fields if field not in response]
        
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        
        return True, ""

# Global validator instance
validator = InputValidator()

# Convenience functions
def sanitize_text(text: str) -> str:
    """Convenience function for text sanitization"""
    return validator.sanitize_text(text)

def validate_review(text: str) -> Tuple[bool, str]:
    """Convenience function for single review validation"""
    return validator.validate_review_text(text)

def validate_batch(reviews: List[str]) -> Tuple[bool, str, List[str]]:
    """Convenience function for batch validation"""
    return validator.validate_review_batch(reviews)