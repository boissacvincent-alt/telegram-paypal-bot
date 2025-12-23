import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# --- CONFIG ---
TOKEN = os.environ.get("BOT_TOKEN")  # Ton token Telegram
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # URL de ton service Render
PAYPAL_LINK = "https://paypal.me/stellaengie"  # Lien PayPal pour paiement

# --- COMMANDES ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Envoie le message de démarrage avec le bouton de paiement.
    """
    keyboard = [
        [InlineKeyboardButton("💳 Payer 20€ via PayPal", url=PAYPAL_LINK)]
    ]
    await update.message.reply_text(
        "🔒 Accès au canal privé\n\n💰 Prix : 20€ (paiement unique)",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- MAIN ---
async def main():
    """
    Crée l'application, configure le webhook et lance le bot.
    """
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Enregistrement automatique du webhook
    await app.bot.set_webhook(f"{WEBHOOK_URL}/webhook/{TOKEN}")

    # Lancement du webhook
    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),  # Render détecte automatiquement le port
        webhook_url=f"{WEBHOOK_URL}/webhook/{TOKEN}"
    )

if __name__ == "__main__":
    asyncio.run(main())
