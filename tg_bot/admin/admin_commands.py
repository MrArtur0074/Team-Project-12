from aiogram import Router, F, types
from .key_boards import start_kb, admin_kb
from aiogram.filters import Command
from tg_bot.config import teachers, admin_command, db, admin

admin_router = Router()

@admin_router.message(Command("start"))
async def start(message: types.Message):
    if message.from_user.id == admin:
        await message.answer(f"Здравствуйте! {message.from_user.full_name}", reply_markup=admin_kb)
    if message.from_user.id in teachers:
        await message.answer(f"Здравствуйте! {message.from_user.full_name}", reply_markup=start_kb)


@admin_router.message(Command(admin_command))
async def new_admin(message: types.Message):
    if not admin:
        db.set_admin({"admin_id":message.from_user.id})
        await message.answer("Вы назначены админом данной системы", reply_markup=admin_kb)