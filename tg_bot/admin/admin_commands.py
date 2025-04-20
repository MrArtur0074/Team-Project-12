from aiogram import Router, types
from .key_boards import start_kb, admin_kb
from aiogram.filters import Command
from tg_bot.config import admin_command, db

admin_router = Router()

@admin_router.message(Command("start"))
async def start(message: types.Message):
    if db.get_admin() and message.from_user.id == db.get_admin()[1]:
        await message.answer(f"Здравствуйте! {message.from_user.full_name}", reply_markup=admin_kb)
    elif message.from_user.id in [i[1] for i in db.get_teachers()]:
        await message.answer(f"Здравствуйте! {message.from_user.full_name}", reply_markup=start_kb)


@admin_router.message(Command(admin_command))
async def new_admin(message: types.Message):
    if not db.get_admin()[1] if db.get_admin() else False:
        db.new_teacher({"tg_id":message.from_user.id})
        db.set_admin({"admin_id":message.from_user.id})
        await message.answer("Вы назначены админом данной системы", reply_markup=admin_kb)
