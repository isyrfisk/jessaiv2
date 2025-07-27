import unittest
from unittest.mock import MagicMock, patch
from core.twilio_handler import TwilioHandler

class TestTwilioHandler(unittest.TestCase):
    def setUp(self):
        self.config = {
            "twilio_account_sid": "test_sid",
            "twilio_auth_token": "test_token",
            "twilio_phone_number": "+1234567890",
            "allowed_phone_numbers": ["+1234567890"],
            "message_rate_limit": 2
        }

    @patch('core.twilio_handler.Client')  # Patch where Client is imported!
    def test_send_message_success(self, mock_client):
        mock_messages = MagicMock()
        mock_client.return_value.messages = mock_messages
        handler = TwilioHandler(self.config)  # Create handler after patching!
        result = handler.send_message("+1234567890", "Test message")
        self.assertTrue(mock_messages.create.called)

    def test_rate_limiting(self):
        handler = TwilioHandler(self.config)
        self.assertTrue(handler._check_rate_limit("+1234567890"))
        self.assertTrue(handler._check_rate_limit("+1234567890"))
        self.assertFalse(handler._check_rate_limit("+1234567890"))

    def test_authorization(self):
        handler = TwilioHandler(self.config)
        self.assertTrue(handler.is_authorized_number("+1234567890"))
        self.assertFalse(handler.is_authorized_number("+1987654321"))

if __name__ == '__main__':
    unittest.main()