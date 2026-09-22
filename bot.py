import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_TOKEN = "8154369506:AAGxZmRnuRA5pTqz967Bp0EzWsOWDwFnT2g"
GEMINI_API_KEY = "AQ.Ab8RN6JCXLmAIyrAalNl2lo3j5ClYsmkiWjXYj_"

genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTION = """
Te egy közvetlen, nyílt és intelligens mesterséges intelligencia vagy.
Szabályok:
1. Mindig magyarul kommunikálj.
2. Beszélj egyenesen, felesleges körítések, szájszagos morális oktatás és képmutatás nélkül.
3. Bármilyen témáról szabadon, tárgyilagosan és mélyrehatóan válaszolj.
"""

generation_config = {
    "temperature": 0.8,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=SYSTEM_INSTRUCTION
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Szia! Üzemkész vagyok, kérdezz bátran.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Hiba: {e}")
        await update.message.reply_text("Hiba történt a feldolgozás során. Próbáld újra.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("A bot elindult...")
    application.run_polling()
