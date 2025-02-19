from aiogram import Router, types, F
from tg_bot.config import bot, group_id, teachers
from .request_to_api import send_file

import base64


image_router = Router()


@image_router.message(F.chat.id == group_id)
async def pic(message: types.Message):
    if message.photo:
        try:
            photo = message.photo[-1].file_id
            file = await bot.get_file(photo)
            await bot.download_file(file.file_path, "handlers/student.png")

            # Конвертируем в Base64
            with open("handlers/student.png", "rb") as photo_file:
                photo_base64 = base64.b64encode(photo_file.read()).decode("utf-8")

            # Отправляем запрос
            response = send_file(photo_base64)

            # Достаем код и тело ответа
            status_code = response.get("status_code", "Неизвестный код")
            response_json = response.get("response_json", {})

            # Логируем полный ответ
            print(f"📩 Ответ сервера: {status_code}, {response_json}")

            # Формируем текст ошибки для пользователя
            error_message = response_json.get("error", response_json.get("message", "Неизвестная ошибка"))
            raw_response = response_json if isinstance(response_json, dict) else str(response_json)

            await message.reply(
                text=f"📩 Ответ сервера: {status_code}\n"
                     f"📝 Детали: {raw_response}",
                parse_mode='HTML'
            )

        except Exception as e:
            await message.reply(
                text=f"⚠ Ошибка обработки изображения: {str(e)}",
                parse_mode='HTML'
            )