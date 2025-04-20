from aiogram import Router, types, F
from tg_bot.config import bot, db
from .request_to_api import send_file
import base64

image_router = Router()

@image_router.message()
async def pic(message: types.Message):
    allowed_chats = [group[0] for group in db.get_groups()]
    if message.chat.id not in allowed_chats:
        return

    admin_id = db.get_admin()[1] if db.get_admin() else None
    teacher_ids = [t[1] for t in db.get_teachers()]
    if message.from_user.id != admin_id and message.from_user.id not in teacher_ids:
        return

    if not message.photo:
        return

    try:
        photo = message.photo[-1].file_id
        file = await bot.get_file(photo)
        await bot.download_file(file.file_path, "group/student.png")

        with open("group/student.png", "rb") as photo_file:
            photo_base64 = base64.b64encode(photo_file.read()).decode("utf-8")

        response = send_file(photo_base64, message.caption if message.caption and message.caption.isdigit() else None)

        status_code = response.get("status_code", "Неизвестный код")
        response_json = response.get("response_json", {})

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
        print(e)
        await message.reply(
            text=f"❌ Ошибка обработки: {str(e)}",
            parse_mode="HTML"
        )
