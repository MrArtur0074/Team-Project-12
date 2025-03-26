import asyncio
import logging
from config import bot, dp, set_commands
from handlers import image_router

# async def on_startup(dispatcher):
#     print('Бот вышел в онлайн')


async def main():
    await set_commands()
    # dp.include_router(start_router)
    # dp.include_router(pictures_router)
    # dp.include_router(free_lesson_reg_router)
    # dp.include_router(courses_router)
    # dp.include_router(scheduler_router)
    # dp.include_router(group_administration_router)

    dp.include_router(image_router)
    # dp.startup.register(on_startup)
    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())