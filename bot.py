from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ваш Telegram-бот. Чем могу помочь?")

# Обработчик данных от Mini App
async def handle_web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем данные из Mini App
    web_app_data = update.message.web_app_data
    if web_app_data:
        try:
            # Парсим JSON-данные
            data = json.loads(web_app_data.data)
            token = data.get('token')

            if token:
                # Обрабатываем токен (например, сохраняем в базу данных или проверяем)
                await update.message.reply_text(f"Токен получен: {token}")
            else:
                await update.message.reply_text("Токен не найден в данных.")
        except json.JSONDecodeError:
            await update.message.reply_text("Ошибка при обработке данных.")
    else:
        await update.message.reply_text("Данные от Mini App не получены.")

# Основная функция
if __name__ == '__main__':
    # Создаем приложение и передаем токен бота
    application = ApplicationBuilder().token("ВАШ_ТОКЕН_БОТА").build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))  # Команда /start
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app_data))  # Данные от Mini App

    # Запускаем бота
    application.run_polling()