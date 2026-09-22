import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# Naplózás beállítása
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Itt adjuk meg a kulcsot, amit az AI Studióban láttál (az AQ.-val kezdődőt)
genai.configure(api_key="AQ.Ab8RN6JFVu61m3r61GXMeRzGJBZ...") 

# Használjuk a stabil ingyenes flash modellt
model = genai.GenerativeModel('gemini-1.5-flash')

# A helyes Telegram tokened (amit a BotFather adott)
TELEGRAM_TOKEN = "8154369506:AAGxZmRnuRA5pTqz967Bp0EzWsOWDwFnT2g"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    logging.info(f"Bejövő üzenet: {user_message}")
    
    try:
        response = model.generate_content(user_message)
        bot_reply = response.text
    except Exception as e:
        logging.error(f"Hiba a Gemini hívás közben: {e}")
        bot_reply = "Sajnálom, hiba történt a válasz generálása közben."
        
    await update.message.reply_text(bot_reply)

def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("A bot elindult és figyel...")
    application.run_polling()

if __name__ == '__main__':
    main()

