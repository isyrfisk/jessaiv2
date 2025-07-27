import logging
from typing import Dict, List
from pathlib import Path
import json

logger = logging.getLogger(__name__)

class ConversationLogger:
    """Handles logging and persistence of conversations"""
    
    @staticmethod
    def sanitize_phone_number(phone_number: str) -> str:
        """Sanitize phone number for filename use"""
        return ''.join(filter(str.isdigit, phone_number))
        
    @staticmethod
    def log_conversation(phone_number: str, messages: List[Dict]):
        """Log conversation to file"""
        try:
            sanitized_number = ConversationLogger.sanitize_phone_number(phone_number)
            log_dir = Path("data/conversation_logs")
            log_dir.mkdir(parents=True, exist_ok=True)
            
            log_file = log_dir / f"{sanitized_number}.json"
            
            with open(log_file, 'a') as f:
                json.dump({
                    "timestamp": str(datetime.now()),
                    "messages": messages
                }, f)
                f.write("\n")
        except Exception as e:
            logger.error(f"Error logging conversation: {e}")