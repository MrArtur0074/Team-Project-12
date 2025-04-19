from aiogram import Bot, Dispatcher, types
from decouple import config
from db.sql_q import DB

TOKEN = config("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

db = DB()
admin = db.get_admin()[1] if db.get_admin() else False
admin_command = config('ADMIN_KEY')

async def set_commands():

    await bot.set_my_commands([
        types.BotCommand(command="start", description="Старт"),
    ])