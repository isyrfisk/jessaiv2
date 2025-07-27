import unittest
from unittest.mock import MagicMock, patch
from core.twilio_handler import TwilioHandler
from datetime import datetime, timedelta

class TestTwilioHandler(unittest.TestCase):
    def setUp(self):
        self.config = {
            "twilio_account_sid": "test_sid",
            "twilio_auth_token": "test_token",
            "twilio_phone_number": "+1234567890",
            "allowed_phone_numbers": ["+1234567890"],
            "message_rate_limit": 2
        }
        self.handler = TwilioHandler(self.config)
        
    @patch('twilio.rest.Client')
    def test_send_message_success(self, mock_client):
        mock_messages = MagicMock()
        mock_client.return_value.messages = mock_messages
        
        result = self.handler.send_message("+1234567890", "Test message")
        self.assertTrue(result)
        
    def test_rate_limiting(self):
        # First message should pass
        self.assertTrue(self.handler._check_rate_limit("+1234567890"))
        
        # Second message should pass
        self.assertTrue(self.handler._check_rate_limit("+1234567890"))
        
        # Third message should fail (limit is 2)
        self.assertFalse(self.handler._check_rate_limit("+1234567890"))
        
    def test_authorization(self):
        self.assertTrue(self.handler.is_authorized_number("+1234567890"))
        self.assertFalse(self.handler.is_authorized_number("+1987654321"))

if __name__ == '__main__':
    unittest.main()