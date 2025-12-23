import os
from flask import Flask, request, jsonify
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
PAYPAL_LINK = "https://paypal.me/stellaengie"

# ---------- TELEGRAM ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("💳 Payer 20€ via PayPal", url=PAYPAL_LINK)
    ]]
    await update.message.reply_text(
        "🔒 Accès au canal privé\n\n💰 Prix : 20€ (paiement unique)",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def run_telegram():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

# ---------- PAYPAL WEBHOOK ----------
flask_app = Flask(__name__)

@flask_app.route("/paypal-webhook", methods=["POST"])
def paypal_webhook():
    data = request.json
    print("Webhook PayPal reçu :", data)
    return jsonify({"status": "ok"})

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

# ---------- MAIN ----------
if __name__ == "__main__":
    Thread(target=run_flask).start()
    run_telegram()
