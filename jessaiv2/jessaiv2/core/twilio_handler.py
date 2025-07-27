# /workspaces/jessaiv2/jessaiv2/core/twilio_handler.py
from twilio.rest import Client

class TwilioHandler:
    def __init__(self, config):
        self.client = Client(config['twilio_account_sid'], config['twilio_auth_token'])
        self.phone_number = config['twilio_phone_number']
    
    def send_message(self, to, body):
        return self.client.messages.create(
            body=body,
            from_=self.phone_number,
            to=to
        )