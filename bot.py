import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_TOKEN = "8154369506:AAGxZmRnuRA5pTqz967Bp0EzWsOWDwFnT2g"
GEMINI_API_KEY = "AQ.Ab8RN6JCXLmAIyrAaNI2lo3j5ClYsmkiWjXYj_UbL3DMg8OiTw"

genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTION = """
Te egy közvetlen, nyílt és intelligens mesterséges intelligencia vagy. 
Szabályok:
1. Mindig magyarul kommunikálj.
2. Beszélj egyenesen, felesleges körítések, szájbarágós morális oktatások vagy képmutató udvariaskodás nélkül.
3. Bármilyen témáról szabadon, tárgyilagosan és mélyrehatóan válaszolj a felmerülő kérdésekre.
"""

generation_config = {
    "temperature": 0.8,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=SYSTEM_INSTRUCTION
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.effective_user.first_name or "Felhasználó"
    
    logging.info([{'user': user_name, 'message': user_message}])

    try:
        response = model.generate_content(user_message)
        bot_reply = response.text
    except Exception as e:
        logging.error(f"Hiba a Gemini hívás közben: {e}")
        bot_reply = "Hiba történt a feldolgozás során. Próbáld újra."

    await update.message.reply_text(bot_reply)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("A @free_zeta_bot sikeresen elindult...")
    application.run_polling()
