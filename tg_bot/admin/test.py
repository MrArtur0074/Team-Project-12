from aiogram import Router, html, F
from aiogram.enums import ChatType
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.message(F.user_shared)
async def handle_user_shared(message: Message):
    user_id = message.user_shared.user_id
    await message.answer(f"Вы выбрали пользователя с ID: {user_id}")

@router.message(F.chat_shared)
async def handle_chat_shared(message: Message):
    chat_id = message.chat_shared.chat_id
    await message.answer(f"Вы выбрали чат с ID: {chat_id}")
