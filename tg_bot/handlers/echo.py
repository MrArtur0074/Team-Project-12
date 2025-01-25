from aiogram import Router, types
from tg_bot.config import bot
import base64


echo_router = Router()


@echo_router.message()
async def pic(message: types.Message):
    if message.photo:
        photo = message.photo[-1].file_id
        file = await bot.get_file(photo)
        await bot.download_file(file.file_path, "handlers/text.png")
        with open("handlers/text.png", "rb") as photo_file:
            photo_base64 = base64.b64encode(photo_file.read()).decode("utf-8")
        print(photo_base64)
        # TODO SEND BASE64 TO API
        await message.reply(
            text=f"Вы отправили фотку <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>\n\n",
                 # f"Base64 кодировка:\n<code>{photo_base64}</code>",
            parse_mode='HTML'
        )



# @echo_router.message()
# async def echo(message: types.Message):
#     await message.reply(f"Вы написали {message.text}")