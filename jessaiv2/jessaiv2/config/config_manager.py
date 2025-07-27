import json
import os
from typing import Dict, Any
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

class ConfigManager:
    """Centralized configuration management with environment variable fallback"""
    
    DEFAULT_CONFIG = {
        "twilio_account_sid": "",
        "twilio_auth_token": "",
        "twilio_phone_number": "",
        "openai_api_key": "",
        "system_prompt": "You are Jess, a professional AI assistant. Provide concise, helpful responses.",
        "max_tokens": 1500,
        "temperature": 0.7,
        "allowed_phone_numbers": [],
        "message_rate_limit": 10,
        "persist_conversations": True
    }
    
    ENV_MAPPING = {
        "twilio_account_sid": "TWILIO_ACCOUNT_SID",
        "twilio_auth_token": "TWILIO_AUTH_TOKEN",
        "openai_api_key": "OPENAI_API_KEY"
    }
    
    def __init__(self, config_path: str = "config/settings.json"):
        self.config_path = config_path
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration with environment variable fallback"""
        config = self.DEFAULT_CONFIG.copy()
        
        # Load from file if exists
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    file_config = json.load(f)
                    config.update(file_config)
            except Exception as e:
                logger.error(f"Error loading config file: {e}")
        
        # Override with environment variables
        for key, env_var in self.ENV_MAPPING.items():
            if env_value := os.getenv(env_var):
                config[key] = env_value
                
        return config
    
    def get(self, key: str, default=None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)