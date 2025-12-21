from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.environ.get("BOT_TOKEN")
PAYPAL_LINK = "https://paypal.me/stellaengie"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("💳 Payer 20€ via PayPal", url=PAYPAL_LINK)
    ]]
    await update.message.reply_text(
        "🔒 Accès au canal privé\n\n💰 Prix : 20€ (paiement unique)\n\nClique ci-dessous pour payer 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
