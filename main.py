from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers.routers import router
import os
import asyncio


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
password = os.getenv("PASSWORD")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())