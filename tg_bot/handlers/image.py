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

            response = send_file(photo_base64, message.caption if message.caption and message.caption.isdigit() else None)

            # Достаем код и тело ответа
            status_code = response.get("status_code", "Неизвестный код")
            response_json = response.get("response_json", {})

            # Определяем сообщение пользователю
            if status_code == 201:
                response_text = "✅ Успешно: лицо добавлено в базу."
            elif status_code == 400:
                error_message = response_json.get("error", "Некорректные данные.")
                response_text = f"⚠ Ошибка: {error_message}"
            elif status_code == 500:
                response_text = "❌ Ошибка сервера. Попробуйте позже."
            else:
                response_text = "⚠ Неизвестная ошибка. Проверьте данные."

            await message.reply(text=response_text, parse_mode="HTML")

        except Exception as e:
            await message.reply(
                text=f"❌ Ошибка обработки: {str(e)}",
                parse_mode="HTML"
            )
    else:
        print(message.caption)
