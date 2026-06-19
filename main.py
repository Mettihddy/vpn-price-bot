import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

ALANCHAND_URL = "https://alanchand.com/currencies-price/usd"

def get_usd():
    try:
        r = requests.get(ALANCHAND_URL, timeout=10)
        text = r.text

        # خیلی ساده عدد دلار رو از صفحه می‌کشه (fallback ساده)
        import re
        match = re.search(r'(\d[\d,]*)', text)
        if match:
            return int(match.group(1).replace(",", ""))
    except:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 برای قیمت /price رو بزن")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usd = get_usd()

    if not usd:
        await update.message.reply_text("خطا در گرفتن نرخ دلار ❌")
        return

    p10 = int(1.5 * usd)
    p25 = int(2.5 * usd)
    p50 = int(4.5 * usd)

    msg = f"""
💰 نرخ دلار: {usd:,} تومان

📦 10 گیگ: {p10:,}
📦 25 گیگ: {p25:,}
📦 50 گیگ: {p50:,}
"""

    await update.message.reply_text(msg)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))

    app.run_polling()

if __name__ == "__main__":
    main()
