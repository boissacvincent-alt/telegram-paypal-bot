import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]
PORT = int(os.environ.get("PORT", 10000))

PAYPAL_LINK = "https://paypal.me/stellaengie"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("💳 Payer 20€ via PayPal", url=PAYPAL_LINK)]]
    await update.message.reply_text(
        "🔒 Accès au canal privé\n\n💰 Prix : 20€ (paiement unique)",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def log_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("UPDATE REÇU :", update)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, log_all))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=f"webhook/{TOKEN}",          # ⭐ LA CLÉ
        webhook_url=f"{WEBHOOK_URL}/webhook/{TOKEN}",
    )

if __name__ == "__main__":
    main()
