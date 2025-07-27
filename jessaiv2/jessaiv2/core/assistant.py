import openai
from typing import Dict, List, Optional
import logging
from pathlib import Path
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class AIAssistant:
    """Handles AI conversation with context management"""
    
    def __init__(self, config):
        openai.api_key = config.get('openai_api_key')
        self.system_prompt = config.get('system_prompt')
        self.max_tokens = config.get('max_tokens', 1500)
        self.temperature = config.get('temperature', 0.7)
        self.persist_conversations = config.get('persist_conversations', True)
        self.conversations = {}
        
    def _get_conversation_file(self, conversation_id: str) -> Path:
        """Get path to conversation history file"""
        return Path(f"data/user_data/{conversation_id}.json")
        
    def _load_conversation(self, conversation_id: str) -> List[Dict]:
        """Load conversation history from file"""
        if not self.persist_conversations:
            return []
            
        file_path = self._get_conversation_file(conversation_id)
        try:
            if file_path.exists():
                with open(file_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading conversation: {e}")
        return []
        
    def _save_conversation(self, conversation_id: str, messages: List[Dict]):
        """Save conversation history to file"""
        if not self.persist_conversations:
            return
            
        file_path = self._get_conversation_file(conversation_id)
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w') as f:
                json.dump(messages, f)
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")
            
    def generate_response(self, user_input: str, conversation_id: str) -> str:
        """Generate AI response with context management"""
        try:
            # Initialize or load conversation
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = self._load_conversation(conversation_id)
                if not self.conversations[conversation_id]:
                    self.conversations[conversation_id] = [
                        {"role": "system", "content": self.system_prompt}
                    ]
                    
            # Add user message
            self.conversations[conversation_id].append(
                {"role": "user", "content": user_input}
            )
            
            # Generate response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.conversations[conversation_id],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            ai_response = response.choices[0].message.content
            
            # Add AI response
            self.conversations[conversation_id].append(
                {"role": "assistant", "content": ai_response}
            )
            
            # Save conversation
            self._save_conversation(conversation_id, self.conversations[conversation_id])
            
            return ai_response
        except Exception as e:
            logger.error(f"AI generation error: {e}")
            return "I encountered an error processing your request. Please try again later."