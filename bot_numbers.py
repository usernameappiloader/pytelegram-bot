from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from twilio.rest import Client
import os

# Configuration Twilio
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Bienvenue! Utilisez /getnumber pour obtenir un numéro de téléphone.')

def get_number(update: Update, context: CallbackContext) -> None:
    number = client.incoming_phone_numbers.create()
    update.message.reply_text(f'Votre numéro est: {number.phone_number}')

def main() -> None:
    updater = Updater(os.getenv('TELEGRAM_BOT_TOKEN'))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("getnumber", get_number))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()