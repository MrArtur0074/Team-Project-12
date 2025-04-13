import asyncio
import logging
from config import bot, dp, set_commands
from group import image_router
from admin import admin_router, router, teacher_router
from db.queries import init_db, create_tables

async def on_startup(dispatcher):
    init_db()
    create_tables()
    print('Бот вышел в онлайн')


async def main():
    await set_commands()
    dp.include_router(admin_router)
    dp.include_router(teacher_router)
    dp.include_router(image_router)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    dp.startup.register(on_startup)
    asyncio.run(main())