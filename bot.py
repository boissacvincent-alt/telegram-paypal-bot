import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import nest_asyncio

# Permet de réutiliser l'event loop déjà existant sur Render
nest_asyncio.apply()

# Variables d'environnement
TOKEN = os.environ.get("BOT_TOKEN")
PAYPAL_LINK = "https://paypal.me/stellaengie"
PORT = int(os.environ.get("PORT", 8443))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # Ex: https://monbot.onrender.com

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("💳 Payer 20€ via PayPal", url=PAYPAL_LINK)]]
    await update.message.reply_text(
        "🔒 Accès au canal privé\n\n💰 Prix : 20€ (paiement unique)",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Fonction principale
async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Enregistrement automatique du webhook
    await app.bot.set_webhook(f"{WEBHOOK_URL}/webhook/{TOKEN}")

    # Lancement du webhook
    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{WEBHOOK_URL}/webhook/{TOKEN}"
    )

# Démarrage du bot
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
