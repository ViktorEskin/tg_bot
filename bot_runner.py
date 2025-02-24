import logging
import asyncio
from openai import AsyncOpenAI
import os

aclient = AsyncOpenAI(api_key= os.getenv("OPENAI_API_KEY"))

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

from youtube_api import get_videos, generate_youtube_links  # Функция для получения видео с YouTube
# from videos import search_videos  # Функция поиска видео в базе
from nltk_helpers import analyze_query  # Функция NLP-анализа текста
from Botai import ai_recommendation  # Функция, использующая GPT-4

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
load_dotenv()

# API токен бота. Получаем токены из .env
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Устанавливаем API-ключ OpenAI (лучше загружать из переменных окружения)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
  # Устанавливаем API-ключ для OpenAI

# Проверяем, загружены ли ключи
if not OPENAI_API_KEY or not API_TOKEN:
    raise ValueError("Необходимо задать OPENAI_API_KEY и TELEGRAM_BOT_TOKEN в .env")


bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

@dp.message(CommandStart())
async def send_welcome(message: Message):
    """Обработчик команды /start."""
    user = message.from_user
    logger.info(f"Пользователь {user.id} ({user.username}) отправил /start")
    await message.answer("Привет! Я помогу тебе найти видео. Напиши тему!")
    logger.info(f"Отправлен ответ пользователю {user.id}")

@dp.message(F.text)
async def handle_message(message: Message):
    """Обрабатывает текстовые сообщения от пользователя."""
    user = message.from_user
    text = message.text.strip() if message.text else ""  # Удаляем лишние пробелы
    query = text  # Определяем query

    logger.info(f"Получено сообщение от {user.id} ({user.username}): {query}")

    if not query:
        await message.answer("Пожалуйста, отправьте текстовое сообщение.")
        return

    # GPT-4o-mini анализ запроса
    # try:
    #     messages = [{"role": "user", "content": query}]
    #     response = await aclient.chat.completions.create(model="gpt-4o-mini",
    #     messages=messages)
    #     ai_reply = response.choices[0].message.content
    #     # await message.answer(ai_reply)
    #     logger.info(f"Смотрим что внутри: {ai_reply}")
    # except Exception as e:
    #     logger.error(f"Ошибка при запросе к OpenAI: {e}")
    #     await message.answer("Произошла ошибка при обработке AI-ответа.")

    # Анализ запроса NLP
    try:
        analysis_result = analyze_query(text)
        logger.info(f"Результат NLP-анализа: {analysis_result}")
    except Exception as e:
        logger.error(f"Ошибка при NLP-анализе: {e}")
        analysis_result = text  # Используем исходный текст в случае ошибки

    # Поиск видео в базе
    # try:
    #     search_results = search_videos(analysis_result)
    #     logger.info(f"Результаты поиска в базе: {search_results}")
    # except Exception as e:
    #     logger.error(f"Ошибка при поиске в базе: {e}")
    #     search_results = "Не удалось найти видео в базе."

    # Получение видео с YouTube
    try:
        youtube_results = get_videos(analysis_result)
        logger.info(f"Результаты поиска на YouTube: {youtube_results}")
    except Exception as e:
        logger.error(f"Ошибка при поиске на YouTube: {e}")
        youtube_results = "Ошибка при получении данных с YouTube."

    # Генерация AI-рекомендации
    try:
        ai_suggestion = ai_recommendation(text)
        logger.info(f"Совет AI: {ai_suggestion}")
    except Exception as e:
        logger.error(f"Ошибка при генерации AI-рекомендации: {e}")
        ai_suggestion = "Не удалось получить рекомендацию."

    # Преобразование в ссылки 
    links = generate_youtube_links(youtube_results)

    

    response_message = (
        f"Вы выбрали тему: {text}\n\n"
        # f"Рекомендованные видео: {search_results}\n\n"
        f"YouTube: \n {links}\n\n"
        f"Совет AI: {ai_suggestion}"
    )
    await message.answer(response_message)
    logger.info(f"Отправлен ответ пользователю {user.id}")

async def main():
    """Запуск бота."""
    try:
        logger.info("Бот запущен и ожидает сообщения.")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

if __name__ == "__main__":
    asyncio.run(main())
