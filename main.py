import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

# Замініть 'YOUR_TELEGRAM_BOT_TOKEN' на свій токен, отриманий від BotFather.
TELEGRAM_TOKEN = '6364052137:AAH7OeYZSH3zcvHP6n2BDyKkHd_Pg_gj5Vk'
OMDB_API_KEY = '70e3fdd0'  # Отримайте ключ API на http://www.omdbapi.com/

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привіт! Відправ мені назву фільму, і я знайду інформацію про нього.")

def search_movie(update, context):
    movie_name = update.message.text
    url = f'http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={movie_name}'
    response = requests.get(url)
    data = response.json()

    if data['Response'] == 'True':
        title = data['Title']
        year = data['Year']
        plot = data['Plot']
        rating = data['imdbRating']

        message = f"Назва: {title}\nРік: {year}\nРейтинг: {rating}\n\nЗміст:\n{plot}"
    else:
        message = "Фільм не знайдено."

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    search_handler = MessageHandler(Filters.text & ~Filters.command, search_movie)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(search_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
