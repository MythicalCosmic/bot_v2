import asyncio
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


def create_socket_with_max_permissions(socket_path):
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

    server = uvicorn.Server(config)

    try:
        server.run()
    except Exception as e:
        logging.error(f"Ошибка при запуске сервера: {e}")
        sys.exit(1)

    try:
        os.chmod(socket_path, 0o777)  # Права чтения, записи и выполнения для всех
        logging.info(f"Установлены права 777 для {socket_path}")
    except Exception as e:
        logging.error(f"Не удалось установить права для socket: {e}")


async def start_polling():
    logging.info("Starting bot in polling mode...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def main():
    socket_path = '/var/www/@Marketing_by_Malika_bot/malika_marketing_bot.sock'

    logging.info(f"Bot is running in {'WEBHOOK' if WEBHOOK else 'POLLING'} mode.")

    if WEBHOOK:
        import threading
        webhook_thread = threading.Thread(
            target=create_socket_with_max_permissions,
            args=(socket_path,)
        )
        webhook_thread.start()
    else:
        await start_polling()


if __name__ == "__main__":
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('/var/www/@Marketing_by_Malika_bot/bot.log'),
            logging.StreamHandler()
        ]
    )
    logging.info("Bot is starting...")

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(main())
