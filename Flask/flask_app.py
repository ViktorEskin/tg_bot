# flask_app.py
from flask import Flask, request, abort
from aiogram.types import Update
import asyncio

from bot_init import dp, bot
import config
import handlers  # где вы регистрируете хендлеры

app = Flask(__name__)

# Подключаем роутер с вашими хендлерами
dp.include_router(handlers.router)

@app.route(config.WEBHOOK_PATH, methods=["POST"])
def telegram_webhook():
    if request.headers.get("content-type") == "application/json":
        data = request.get_data(as_text=True)
        update = Update.parse_raw(data)  # или Update.de_json(data)

        # В aiogram 3.x можно вызывать:
        # create_task + await dp.update.update(...)
        # (зависит от точной версии и сборки 3.x)
        asyncio.get_event_loop().create_task(dp.update.update(bot, update))
        return "OK", 200
    else:
        abort(403)

@app.before_first_request
def setup_webhook():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.delete_webhook())
    loop.run_until_complete(bot.set_webhook(config.WEBHOOK_URL))

if __name__ == "__main__":
    app.run(debug=True)
