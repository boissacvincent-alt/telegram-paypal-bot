import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Récupération des variables d'environnement
TOKEN = os.environ.get("BOT_TOKEN")
PAYPAL_LINK = "https://paypal.me/stellaengie"
PORT = int(os.environ.get("PORT", 8443))          # Render fournit automatiquement le port
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")      # Ex: https://monbot.onrender.com

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("💳 Payer 20€ via PayPal", url=PAYPAL_LINK)]]
    await update.message.reply_text(
        "🔒 Accès au canal privé\n\n💰 Prix : 20€ (paiement unique)",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def main():
    # Création de l'application Telegram
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Configuration du webhook pour Render
    app.run_webhook(
        listen="0.0.0.0",                # Obligatoire pour que Render puisse accéder au port
        port=PORT,
        webhook_url=f"{WEBHOOK_URL}/webhook/{TOKEN}"
    )

if __name__ == "__main__":
    main()
