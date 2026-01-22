import requests
import logging

logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_message(self, message):
        """Sends a text message to the configured Telegram chat."""
        if not self.token or not self.chat_id:
            logger.warning("Telegram credentials not configured. Skipping notification.")
            return

        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(self.base_url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info("Telegram notification sent successfully.")
            else:
                logger.error(f"Failed to send Telegram message: {response.text}")
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
