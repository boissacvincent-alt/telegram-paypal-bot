import os
import secrets
from flask import Flask, request, jsonify
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from threading import Thread

# ========================
# Variables d'environnement
# ========================
TOKEN = os.environ.get("BOT_TOKEN")  # Token Telegram
CHANNEL = "@TON_CANAL_PRIVÉ"         # Ton canal privé
PORT = int(os.environ.get("PORT", 8443))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # Exemple: https://bot-token-ytmt.onrender.com
PAYPAL_LINK = "https://paypal.me/TON_LIEN_PAYPAL"

bot = Bot(TOKEN)
pending_users = {}  # email ou chat_id en attente de paiement

# ========================
# Telegram /start
# ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    # Enregistre l'utilisateur pour le paiement
    pending_users[chat_id] = None  # On n'a pas encore l'email PayPal
    keyboard = [[InlineKeyboardButton("💳 Payer 20€ via PayPal", url=PAYPAL_LINK)]]
    await update.message.reply_text(
        "🔒 Pour accéder au canal privé, payez via PayPal 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ========================
# Webhook PayPal
# ========================
app = Flask(__name__)

@app.route("/paypal-webhook", methods=["POST"])
def paypal_webhook():
    data = request.json
    print("Webhook PayPal reçu:", data)  # Pour voir dans les logs Render

    # Vérifier que le paiement est complet
    if data.get("event_type") == "PAYMENT.SALE.COMPLETED":
        payer_email = data["resource"]["payer"]["email_address"]
        # Ici tu peux associer l'email PayPal avec le chat_id
        # Exemple simplifié : ajouter tous les pending_users
        for chat_id in list(pending_users.keys()):
            try:
                bot.add_chat_members(chat_id=CHANNEL, user_ids=[chat_id])
                bot.send_message(chat_id=chat_id, text="✅ Vous êtes ajouté au canal privé !")
                pending_users.pop(chat_id)
            except Exception as e:
                print("Erreur ajout utilisateur:", e)

    return jsonify({"status": "ok"})

# ========================
# Lancement Telegram et Flask
# ========================
def main():
    # Telegram
    app_telegram = Application.builder().token(TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))

    # Flask dans un thread séparé pour le webhook PayPal
    Thread(target=lambda: app.run(host="0.0.0.0", port=PORT)).start()

    # Lancer Telegram en polling
    app_telegram.run_polling()

if __name__ == "__main__":
    main()
