from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from flask import Flask, request
from twilio.rest import Client
import os

# Configuration Twilio
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

app = Flask(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Bienvenue! Utilisez /send_sms pour envoyer un SMS.')

def send_sms(update: Update, context: CallbackContext) -> None:
    phone_number = context.args[0] if context.args else None
    message_body = context.args[1] if len(context.args) > 1 else None

    if not phone_number or not message_body:
        update.message.reply_text('Veuillez fournir un numéro de téléphone et un message. Exemple: /send_sms +1234567890 "Votre message"')
        return

    message = client.messages.create(
        body=message_body,
        from_=os.getenv('TWILIO_PHONE_NUMBER'),
        to=phone_number
    )
    update.message.reply_text(f'SMS envoyé avec l\'ID: {message.sid}')

def sms_reply():
    message_body = request.form['Body']
    # Traitez le message reçu ici
    return 'Message reçu', 200

@app.route('/sms', methods=['POST'])
def webhook():
    return sms_reply()

def main() -> None:
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("send_sms", send_sms))

    application.run_polling()
    app.run(debug=True)

if __name__ == '__main__':
    main()
