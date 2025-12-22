from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# Récupère le token depuis la variable d'environnement
TOKEN = os.environ.get("BOT_TOKEN")

# Lien PayPal
PAYPAL_LINK = "https://paypal.me/stellaengie"

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("💳 Payer 20€ via PayPal", url=PAYPAL_LINK)
    ]]
    await update.message.reply_text(
        "🔒 Accès au canal privé\n\n💰 Prix : 20€ (paiement unique)",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

if __name__ == "__main__":
    # Crée l'application Telegram
    app = Application.builder().token(TOKEN).build()
    
    # Ajoute le handler /start
    app.add_handler(CommandHandler("start", start))
    
    # Démarre le bot
    app.run_polling()
