from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask
import threading

TOKEN = "8417773265:AAFhYBVD6bOgVgEpGjGB6dVisJzIdi5Uce4"
ADMIN_ID = 6580598992

# Твой код бота (оставь без изменений, только дополним внизу)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Отправь сюда сообщение — я передам его администратору *анонимно*.",
        parse_mode="Markdown"
    )

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ У вас нет прав для этой команды.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("❗ Используй формат: /reply user_id сообщение")
        return

    try:
        user_id = int(context.args[0])
        reply_text = " ".join(context.args[1:])
        await context.bot.send_message(chat_id=user_id, text=f"💬 Ответ от администратора:\n\n{reply_text}")
        await update.message.reply_text("✅ Ответ отправлен пользователю.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка при отправке: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    name = user.full_name or "Без имени"
    username = f"@{user.username}" if user.username else "(username отсутствует)"
    user_id = user.id

    admin_msg = (
        f"📨 Новое анонимное сообщение:\n\n"
        f"{text}\n\n"
        f"👤 Имя: {name}\n"
        f"🔗 Username: {username}\n"
        f"🆔 ID: {user_id}\n\n"
        f"🔁 Чтобы ответить, используй:\n"
        f"/reply {user_id} твой_ответ_сюда"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_msg)
    await update.message.reply_text("✅ Ваше сообщение отправлено анонимно!")

# Запускаем Flask — простой сервер для Render
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot is running!"

def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", reply))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

def main():
    # Запускаем бот в отдельном потоке
    threading.Thread(target=run_bot).start()
    # Запускаем Flask сервер, который слушает 0.0.0.0:8000
    app_flask.run(host='0.0.0.0', port=8000)

if __name__ == "__main__":
    main()


