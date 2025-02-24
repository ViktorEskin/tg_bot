# bot_init.py
import config
from aiogram.client.bot import Bot, DefaultBotProperties
from aiogram import Dispatcher

bot = Bot(
    token=config.TELEGRAM_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()
