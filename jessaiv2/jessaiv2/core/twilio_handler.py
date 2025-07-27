import os
from dotenv import load_dotenv
from core.twilio_handler import TwilioHandler

# Load environment variables from .env
load_dotenv()

config = {
    "twilio_account_sid": os.getenv("TWILIO_ACCOUNT_SID"),
    "twilio_auth_token": os.getenv("TWILIO_AUTH_TOKEN"),
    "twilio_phone_number": os.getenv("TWILIO_PHONE_NUMBER"),
    "allowed_phone_numbers": [os.getenv("TWILIO_PHONE_NUMBER")],  # or your recipient
    "message_rate_limit": 10
}

handler = TwilioHandler(config)

# Replace with the recipient's real phone number
to_number = "+60183420125"  # Example: your own number for testing
message = "Hello from your real Twilio API call!"

result = handler.send_message(to_number, message)
print("Message sent! SID:", result.sid)