from aiogram import Bot, Dispatcher, types


TOKEN = '5838613898:AAHmQ1yecxVHDuyFw9cDFst4fCI_yzD3T5k'
bot = Bot(token=TOKEN)
dp = Dispatcher()
group_id = -4624968539
teachers = [656051677, 396952302, 1373122571, 1154757842]


async def set_commands():
    """
    Настройка команд
     в меню бота
    """
    # строка выше наз-ся Docstring
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Старт"),
        # types.BotCommand(command="pic", description="Отправить картинку"),
        # types.BotCommand(command="courses", description="Наши курсы"),
        # types.BotCommand(command="lesson", description="Записаться на пробный урок"),
    ])