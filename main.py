import asyncio
import logging
import uvicorn
from fastapi import FastAPI
from aiogram.types import Update
from config.config import bot, dp
from config.settings import WEBHOOK, WEBHOOK_URL

app = FastAPI()


@app.post("/webhook")
async def webhook(update: dict):
    tg_update = Update(**update)
    await dp.feed_update(bot, tg_update)
    return {"status": "ok"}


async def start_webhook():
    logging.info("Starting bot in webhook mode...")
    config = uvicorn.Config(
        app,
        uds='/app/malika_marketing_bot.sock',
        workers=2,
        limit_max_requests=1000,
        timeout_keep_alive=120
    )
    import os
    import stat

    server = uvicorn.Server(config)

    # Создаем socket перед запуском сервера
    await server.startup()

    # Устанавливаем максимально открытые права
    os.chmod('/app/bot.sock', stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    await server.serve()


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
