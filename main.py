# Конфигурационные библиотеки
from dotenv import load_dotenv

# Встроенные библиотеки
import os

# Сторонние библиотеки
from telebot import TeleBot
from source.AIReviewer import AIReviewer
from source.FileExtractor import FileExtractor
from source.ReviewShaper import ReviewShaper
from source.File import File, FileType

# Загрузка переменных окружения
load_dotenv()
API = os.getenv('API')
BOT_TOKEN = os.getenv('BOT_TOKEN')
MODEL_TOKEN = os.getenv('MODEL_TOKEN')

# Локгика Telegram-Бота
bot = TeleBot(BOT_TOKEN)
WELCOM_MESSAGE = '''
Привет! Я AI-Ассистент, помогающий людям ускорять работу
по анализу кода на соответсвие корпоративным стандартам и
на выявление уязвимостей и ошибок.

Чтобы начать работу, отправь файл .cs или архив проекта С#!
Я проанализирую твой код и скину тебе отчет!
'''

@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    file_content = bot.download_file(file_info.file_path)
    file_type = FileType.Archive if file_name.endswith('.zip') else FileType.File
    file = File(file_type, message.document.file_name, file_content, list())
    
    reviewer = AIReviewer(API, MODEL_TOKEN)
    file_extractor = FileExtractor()
    review_shaper = ReviewShaper()
    reviews = []
    
    files_to_review = file_extractor.extract(file)
    for content in files_to_review:
        if file_type == FileType.Archive:
            for fl in file.neasted:
                _message = reviewer.review(fl.content)
                review = [ review_shaper.generate_review(fl, _message) ]
                reviews.append(review)
        else:
            _message = reviewer.review(content)
            review = [ review_shaper.generate_review(file, _message) ]
            reviews.append(review)

    bot.reply_to(message, f"Ваш {file_type} был обработан, результаты прикреплены к сообщению.")
    for rev in reviews:
        for pathTo in rev:
            with open(pathTo, "rb") as review:
                bot.send_document(chat_id=message.chat.id, document=review)
            os.remove(pathTo)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, WELCOM_MESSAGE)

@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.reply_to(message, "Я не знаю, что делать с этим. Пожалуйста, отправьте мне файл или архив для обработки.")

if __name__ == '__main__':
    print("Bot started")
    bot.infinity_polling()