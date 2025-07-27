# jessaiv2/app.py

# Absolute imports (recommended)
from jessaiv2.config.config_manager import ConfigManager
from jessaiv2.core.assistant import AIAssistant
from jessaiv2.core.utilities import ConversationLogger
from jessaiv2.core.twilio_handler import TwilioHandler  # If you have this

# Alternative relative imports (only use if app.py is inside jessaiv2/)
# from .config.config_manager import ConfigManager
# from .core.assistant import AIAssistant

# Initialize components
config = ConfigManager()
assistant = AIAssistant(config.config)
twilio = TwilioHandler(config.config)

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jess_ai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('JessAI')

# Initialize components
config = ConfigManager()
twilio = TwilioHandler(config.config)
assistant = AIAssistant(config.config)

@app.route('/sms', methods=['POST'])
def sms_handler() -> Response:
    """Handle incoming SMS messages"""
    try:
        from_number = request.form.get('From', '')
        message_body = request.form.get('Body', '').strip()
        
        if not twilio.is_authorized_number(from_number):
            logger.warning(f"Unauthorized access attempt from {from_number}")
            return Response("Unauthorized", status=403)
            
        if not message_body:
            return Response("Empty message", status=400)
            
        # Generate response
        ai_response = assistant.generate_response(message_body, from_number)
        
        # Send response
        if not twilio.send_message(from_number, ai_response):
            return Response("Rate limit exceeded", status=429)
            
        # Log conversation
        ConversationLogger.log_conversation(from_number, [
            {"role": "user", "content": message_body},
            {"role": "assistant", "content": ai_response}
        ])
            
        return Response("", status=200)
    except Exception as e:
        logger.error(f"Handler error: {e}")
        return Response("Server error", status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)