import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
PAYPAL_LINK = "https://paypal.me/stellaengie"

PORT = int(os.environ.get("PORT", 10000))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # ex: https://telegram-paypal-bot-0sf9.onrender.com
WEBHOOK_PATH = f"/webhook/{TOKEN}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("💳 Payer 20€ via PayPal", url=PAYPAL_LINK)
    ]]
    await update.message.reply_text(
        "🔒 Accès au canal privé\n\n💰 Prix : 20€ (paiement unique)",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{WEBHOOK_URL}{WEBHOOK_PATH}",
        webhook_path=WEBHOOK_PATH
    )

if __name__ == "__main__":
    main()
