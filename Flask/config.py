import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # токен от BotFather
WEBHOOK_PATH = "/webhook"     # путь, который будет обрабатывать Flask
USERNAME = "SomeName"         # ваше имя на PythonAnywhere
WEBHOOK_URL = f"https://{USERNAME}.someURL.com{WEBHOOK_PATH}"

