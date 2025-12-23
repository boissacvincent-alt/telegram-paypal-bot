import os
import secrets
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from aiohttp import web

TOKEN = os.environ["BOT_TOKEN"]
PORT = int(os.environ.get("PORT", 10000))
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

PAYPAL_LINK = "https://paypal.me/stellaengie"
BASE_INVITE_LINK = "https://t.me/mon_canal?start="

DB_FILE = "paid_users.db"

# ----------------- Base SQLite -----------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id TEXT PRIMARY KEY,
            token TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_user(telegram_id, token):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (telegram_id, token) VALUES (?, ?)", (telegram_id, token))
    conn.commit()
    conn.close()

# ----------------- Telegram -----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("💳 Payer 20€ via PayPal", url=PAYPAL_LINK)]]
    await update.message.reply_text(
        "🔒 Accès au canal privé\n\n💰 Prix : 20€ (paiement unique)",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ----------------- Webhook PayPal -----------------
async def paypal_webhook_handler(request):
    data = await request.json()
    telegram_id = data.get("custom_telegram_id")  # mettre le Telegram ID lors du paiement
    status = data.get("payment_status") or data.get("status")

    if telegram_id and status == "COMPLETED":
        token = secrets.token_urlsafe(8)
        save_user(telegram_id, token)
        invite_link = f"{BASE_INVITE_LINK}{token}"
        await app.bot.send_message(chat_id=int(telegram_id), text=f"Merci pour ton paiement ! Voici ton lien : {invite_link}")

    return web.Response(text="OK", status=200)

# ----------------- Webhook App -----------------
def create_app():
    app_web = web.Application()
    app_web.router.add_post("/paypal_webhook", paypal_webhook_handler)
    return app_web

# ----------------- Main -----------------
def main():
    global app
    init_db()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, lambda u, c: print("UPDATE REÇU :", u)))
    
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=f"webhook/{TOKEN}",
        webhook_url=f"{WEBHOOK_URL}/webhook/{TOKEN}",
        webhook_app=create_app()
    )

if __name__ == "__main__":
    main()
