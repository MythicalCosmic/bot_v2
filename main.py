import asyncio
import logging
import uvicorn
from fastapi import FastAPI
from aiogram.types import Update
from config.config import bot, dp
from config.settings import WEBHOOK, WEBHOOK_URL
import os
import stat

app = FastAPI()


@app.post("/webhook")
async def webhook(update: dict):
    tg_update = Update(**update)
    await dp.feed_update(bot, tg_update)
    return {"status": "ok"}


def start_webhook():
    logging.info("Starting bot in webhook mode...")

    # Подготовка socket
    socket_path = '/app/malika_marketing_bot.sock'

    # Удаляем существующий сокет, если есть
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

    # Установка прав на socket
    server.run()

    # Если сервер завершился, применяем права
    os.chmod(socket_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)


async def start_polling():
    logging.info("Starting bot in polling mode...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def main():
    logging.info(f"Bot is running in {'WEBHOOK' if WEBHOOK else 'POLLING'} mode.")
    if WEBHOOK:
        # Используем многопоточность для запуска webhook
        import threading
        webhook_thread = threading.Thread(target=start_webhook)
        webhook_thread.start()
    else:
        await start_polling()


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
