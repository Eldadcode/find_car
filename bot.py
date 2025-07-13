import logging
import re
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters
from car_api import CarDataAPI
from config import BOT_TOKEN

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class CarInfoBot:
    def __init__(self):
        self.car_api = CarDataAPI()
    
    def handle_message(self, update: Update, context) -> None:
        """Handle incoming messages and respond with car information"""
        try:
            message_text = update.message.text.strip()
            
            # Skip if message is empty or too short
            if not message_text or len(message_text) < 3:
                return
            
            # Check if the message looks like a license plate
            if self._is_likely_license_plate(message_text):
                self._process_license_plate(update, message_text)
            else:
                # Send help message for non-license plate messages
                self._send_help_message(update)
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            update.message.reply_text(
                "מצטער, נתקלתי בשגיאה בעיבוד הבקשה שלך. אנא נסה שוב."
            )
    
    def _is_likely_license_plate(self, text: str) -> bool:
        """Check if the text looks like an Israeli license plate"""
        # Remove common separators
        cleaned = re.sub(r'[\s\-]', '', text.upper())
        
        # Should contain at least some digits
        if not re.search(r'\d', cleaned):
            return False
        
        return True
    
    def _process_license_plate(self, update: Update, license_plate: str) -> None:
        """Process a license plate and return car information"""
        try:
            # Send typing indicator
            update.message.reply_chat_action("typing")
            
            # Search for car information
            car_data = self.car_api.search_car_by_license_plate(license_plate)
            
            if car_data:
                # Format and send car information
                car_info = self.car_api.format_car_info(car_data)
                response = f"🚗 **מידע על הרכב** 🚗\n\n{car_info}"
                
                update.message.reply_text(
                    response,
                    parse_mode='Markdown'
                )
            else:
                # No car found
                update.message.reply_text(
                    f"❌ לא נמצא מידע על רכב עם מספר רישוי: **{license_plate}**\n\n"
                    "אנא בדוק את מספר הרישוי ונסה שוב.",
                    parse_mode='Markdown'
                )
                
        except Exception as e:
            logger.error(f"Error processing license plate: {e}")
            update.message.reply_text(
                "מצטער, נתקלתי בשגיאה בחיפוש מידע על הרכב. אנא נסה שוב."
            )
    
    def _send_help_message(self, update: Update) -> None:
        """Send help message for non-license plate messages"""
        help_text = (
            "🚗 **בוט מידע על רכבים** 🚗\n\n"
            "פשוט שלח לי מספר רישוי ישראלי ואני אספק לך מידע על הרכב!\n\n"
            "**דוגמאות:**\n"
            "• 12-345-67\n"
            "• 123-45-678\n"
            "• 1234567\n\n"
            "הבוט יזהה אוטומטית מספרי רישוי ויענה עם פרטי הרכב כולל:\n"
            "• יצרן\n"
            "• דגם\n"
            "• שנת ייצור\n"
            "• צבע\n"
            "• פרטי מנוע\n"
            "• סוג דלק"
        )
        
        update.message.reply_text(
            help_text,
            parse_mode='Markdown'
        )

def main() -> None:
    """Start the bot"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found in environment variables!")
        return
    
    # Create bot instance
    bot = CarInfoBot()
    
    # Create updater
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    # Add message handler for all text messages
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, bot.handle_message)
    )
    
    # Start the bot
    logger.info("Starting Car Information Bot...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main() 