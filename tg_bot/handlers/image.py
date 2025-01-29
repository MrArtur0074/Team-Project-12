from aiogram import Router, types, F
from tg_bot.config import bot, group_id, teachers
from .request_to_api import send_file

import base64


image_router = Router()


@image_router.message(F.chat.id == group_id)
async def pic(message: types.Message):
    if message.photo:
        photo = message.photo[-1].file_id
        file = await bot.get_file(photo)
        await bot.download_file(file.file_path, "handlers/student.png")
        with open("handlers/student.png", "rb") as photo_file:
            photo_base64 = base64.b64encode(photo_file.read()).decode("utf-8")
        response = send_file(photo_base64)
        await message.reply(
            text=f"Вы отправили фотку <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>\n\n"
                 f"Response code {response}",
            parse_mode='HTML'
        )

