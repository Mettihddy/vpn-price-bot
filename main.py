import os
import requests
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ===== TOKEN =====
TOKEN = os.getenv("BOT_TOKEN")

# ===== URL دلار =====
ALANCHAND_URL = "https://alanchand.com/currencies-price/usd"


# ===== گرفتن قیمت دلار (امن) =====
def get_usd():
    try:
        r = requests.get(ALANCHAND_URL, timeout=10)
        text = r.text

        match = re.search(r'(\d[\d,]*)', text)

        if match:
            return int(match.group(1).replace(",", ""))

        return None

    except Exception as e:
        print("USD ERROR:", e)
        return None


# ===== /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋\nبرای قیمت /price رو بزن")


# ===== /price =====
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usd = get_usd()

    if not usd:
        await update.message.reply_text("❌ خطا در گرفتن قیمت دلار")
        return

    # قیمت‌ها (سود نیم دلاری تو لحاظ شده)
    p10 = int((1.5) * usd)
    p25 = int((2.5) * usd)
    p50 = int((4.5) * usd)

    msg = f"""
💰 نرخ دلار: {usd:,} تومان

📦 10 گیگ: {p10:,} تومان
📦 25 گیگ: {p25:,} تومان
📦 50 گیگ: {p50:,} تومان
"""

    await update.message.reply_text(msg)


# ===== main =====
def main():
    if not TOKEN:
        print("BOT TOKEN NOT FOUND!")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
