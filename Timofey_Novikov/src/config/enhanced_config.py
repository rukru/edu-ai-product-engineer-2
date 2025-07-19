"""
Enhanced Configuration Manager
Handles all application configuration with graceful degradation
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from ..constants import DEFAULT_CONFIG, ERROR_MESSAGES, LOG_CONFIG

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_CONFIG['level']),
    format=LOG_CONFIG['format']
)
logger = logging.getLogger(__name__)

class EnhancedConfigManager:
    """Manages application configuration with fallbacks and validation"""
    
    def __init__(self):
        self._config = self._load_config()
        self._warnings = []
        self._validate_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment and files with fallbacks"""
        config = {
            # OpenAI Configuration
            'openai_api_key': os.getenv('OPENAI_API_KEY'),
            'openai_model': os.getenv('OPENAI_MODEL', DEFAULT_CONFIG['openai_model']),
            'openai_max_tokens': int(os.getenv('OPENAI_MAX_TOKENS', str(DEFAULT_CONFIG['max_tokens']))),
            'openai_temperature': float(os.getenv('OPENAI_TEMPERATURE', str(DEFAULT_CONFIG['temperature']))),
            
            # Application Settings
            'debug': os.getenv('DEBUG', 'False').lower() == 'true',
            'log_level': os.getenv('LOG_LEVEL', LOG_CONFIG['level']),
            'max_retries': int(os.getenv('MAX_RETRIES', str(DEFAULT_CONFIG['max_retries']))),
            'timeout': int(os.getenv('TIMEOUT', str(DEFAULT_CONFIG['timeout']))),
            
            # Analysis Settings
            'parallel_processing': os.getenv('PARALLEL_PROCESSING', 'True').lower() == 'true',
            'batch_size': int(os.getenv('BATCH_SIZE', '10')),
            'rate_limit_delay': float(os.getenv('RATE_LIMIT_DELAY', str(DEFAULT_CONFIG['rate_limit_delay']))),
            'max_reviews_per_batch': int(os.getenv('MAX_REVIEWS_PER_BATCH', str(DEFAULT_CONFIG['max_reviews_per_batch']))),
            'max_review_length': int(os.getenv('MAX_REVIEW_LENGTH', str(DEFAULT_CONFIG['max_review_length'])))
        }
        
        # Load from config file if exists
        config_file = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'app_settings.json')
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    file_config = json.load(f)
                    # Only update non-sensitive settings from file
                    safe_keys = ['openai_model', 'openai_max_tokens', 'openai_temperature', 
                               'parallel_processing', 'batch_size', 'max_retries']
                    for key in safe_keys:
                        if key in file_config:
                            config[key] = file_config[key]
                logger.info(f"Loaded configuration from {config_file}")
            except Exception as e:
                logger.warning(f"Could not load config file: {e}")
        
        return config
    
    def _validate_config(self):
        """Validate configuration and collect warnings"""
        # Check OpenAI API availability
        if not self._config.get('openai_api_key'):
            warning = ERROR_MESSAGES['openai_api_unavailable']
            self._warnings.append(warning)
            logger.warning(warning)
        
        # Check token limits
        if self._config.get('openai_max_tokens', 0) > 4000:
            warning = "OpenAI max_tokens is very high. This may increase costs significantly."
            self._warnings.append(warning)
            logger.warning(warning)
        
        # Validate batch size
        if self._config.get('batch_size', 0) > 100:
            self._config['batch_size'] = 100
            warning = "Batch size reduced to maximum of 100 for performance."
            self._warnings.append(warning)
            logger.warning(warning)
        
        # Validate rate limits
        if self._config.get('rate_limit_delay', 0) < 0.1:
            self._config['rate_limit_delay'] = 0.1
            warning = "Rate limit delay increased to minimum of 0.1s to prevent API throttling."
            self._warnings.append(warning)
            logger.warning(warning)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with fallback"""
        return self._config.get(key, default)
    
    def is_openai_available(self) -> bool:
        """Check if OpenAI API is properly configured"""
        return bool(self._config.get('openai_api_key'))
    
    def get_openai_config(self) -> Dict[str, Any]:
        """Get OpenAI-specific configuration"""
        return {
            'api_key': self._config.get('openai_api_key'),
            'model': self._config.get('openai_model'),
            'max_tokens': self._config.get('openai_max_tokens'),
            'temperature': self._config.get('openai_temperature')
        }
    
    def get_warnings(self) -> list:
        """Get configuration warnings"""
        return self._warnings.copy()
    
    def has_openai_fallback(self) -> bool:
        """Check if system can work without OpenAI API"""
        return True  # Our system has deterministic and agent fallbacks
    
    def get_analysis_config(self) -> Dict[str, Any]:
        """Get analysis-specific configuration"""
        return {
            'parallel_processing': self._config.get('parallel_processing'),
            'max_retries': self._config.get('max_retries'),
            'timeout': self._config.get('timeout'),
            'rate_limit_delay': self._config.get('rate_limit_delay'),
            'max_reviews_per_batch': self._config.get('max_reviews_per_batch'),
            'max_review_length': self._config.get('max_review_length')
        }
    
    def validate_for_production(self) -> bool:
        """Validate configuration for production use"""
        issues = []
        
        if self._config.get('debug'):
            issues.append("Debug mode is enabled")
        
        if not self._config.get('openai_api_key') and not self.has_openai_fallback():
            issues.append("No OpenAI API key and no fallback available")
        
        if self._config.get('log_level') == 'DEBUG':
            issues.append("Log level is set to DEBUG (may expose sensitive data)")
        
        if issues:
            logger.error(f"Production validation failed: {', '.join(issues)}")
            return False
        
        logger.info("Configuration validated for production use")
        return True

# Global enhanced config instance
enhanced_config = EnhancedConfigManager()