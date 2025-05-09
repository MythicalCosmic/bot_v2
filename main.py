import asyncio
import logging
import uvicorn
import os
import sys
from fastapi import FastAPI
from aiogram.types import Update
from config.config import bot, dp
from config.settings import WEBHOOK, WEBHOOK_URL

app = FastAPI()


@app.post("/Marketing_by_Malika_bot")
async def webhook(update: dict):
    tg_update = Update(**update)
    await dp.feed_update(bot, tg_update)
    return {"status": "ok"}


def run_webhook_server(socket_path):
    """
    Функция для запуска webhook сервера в отдельном потоке
    """
    # Удаление существующего сокета
    if os.path.exists(socket_path):
        os.unlink(socket_path)

    config = uvicorn.Config(
        app,
        uds=socket_path,
        workers=1,
        limit_max_requests=1000,
        timeout_keep_alive=120,
        log_level="info"
    )

    try:
        server = uvicorn.Server(config)
        server.run()

        # Установка прав на сокет
        os.chmod(socket_path, 0o777)
    except Exception as e:
        logging.error(f"Ошибка при запуске webhook: {e}")
        sys.exit(1)


async def start_webhook():
    logging.info("Starting bot in webhook mode...")
    socket_path = '/app/malika_marketing_bot.sock'

    # Запуск сервера в отдельном потоке
    import threading
    webhook_thread = threading.Thread(
        target=run_webhook_server,
        args=(socket_path,),
        daemon=True  # Поток завершится вместе с основной программой
    )
    webhook_thread.start()


async def start_polling():
    logging.info("Starting bot in polling mode...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def main():
    logging.info(f"Bot is running in {'WEBHOOK' if WEBHOOK else 'POLLING'} mode.")
    if WEBHOOK:
        await start_webhook()
    else:
        await start_polling()

    # Бесконечное ожидание, чтобы поток webhook не завершился
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    import asyncio
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.info("Bot is starting...")

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(main())
