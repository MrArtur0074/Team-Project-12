import asyncio
import base64
import uuid
from pathlib import Path
from aiogram.types import FSInputFile
from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import db
from key_boards import cancel_kb, start_kb

from .request import search_by_photo, search_by_id

fsm_router = Router()

class FaceIDCheck(StatesGroup):
    face = State()
    id = State()


@fsm_router.callback_query(F.data == "cancel")
async def cancel_registration(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.clear()
    await call.message.answer("Процесс приостановлен")


@fsm_router.callback_query(F.data == "face_check")
async def face_check(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id not in [i[1] for i in db.get_teachers()]:
        await call.answer("Нет доступа", show_alert=True)
        return

    await call.message.delete()
    await state.set_state(FaceIDCheck.face)
    await call.message.answer("Отправьте лицо студента", reply_markup=cancel_kb)


@fsm_router.callback_query(F.data == "id_check")
async def id_check(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id not in [i[1] for i in db.get_teachers()]:
        await call.answer("Нет доступа", show_alert=True)
        return

    await call.message.delete()
    await state.set_state(FaceIDCheck.id)
    await call.message.answer("Напишите id студента", reply_markup=cancel_kb)


@fsm_router.message(FaceIDCheck.id)
async def id_response(message: types.Message, state: FSMContext):
    if message.from_user.id not in [i[1] for i in db.get_teachers()]:
        await message.answer("Нет доступа")
        return

    await message.delete()
    await state.clear()

    try:
        data, status_code = await asyncio.to_thread(search_by_id, int(message.text))
    except ValueError:
        await message.answer("ID должен быть числом.")
        return

    if status_code == 200 and isinstance(data, list) and data:
        await send_applicant_info(message, data[0])
    elif status_code == 404:
        await message.answer("❌ Пользователь не найден.")
    else:
        await message.answer(f"⚠️ Ошибка при запросе к серверу.\n\n{data.get('error', '')}")

    # Завершение
    await message.answer(
        f"Здравствуйте! {message.from_user.full_name}",
        reply_markup=start_kb
    )


@fsm_router.message(FaceIDCheck.face)
async def face_response(message: types.Message, state: FSMContext):
    if message.from_user.id not in [i[1] for i in db.get_teachers()]:
        await message.answer("Нет доступа")
        return

    await message.delete()
    await state.clear()

    if not message.photo:
        await message.answer("Пожалуйста, отправьте изображение.")
        return

    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    photo_bytes = await message.bot.download_file(file.file_path)

    data, status_code = await asyncio.to_thread(search_by_photo, photo_bytes.read())

    if status_code == 200:
        await send_applicant_info(message, data)
    elif status_code == 403:
        await message.answer("❌ Пользователь в чёрном списке!")
    elif status_code == 404:
        await message.answer("❌ Пользователь не найден.")
    else:
        await message.answer(f"⚠️ Ошибка при запросе к серверу.\n\n{data.get('error', '')}")

    # Завершение
    await message.answer(
        f"Здравствуйте! {message.from_user.full_name}",
        reply_markup=start_kb
    )


async def send_applicant_info(message: types.Message, data: dict):
    text = (
        f"👤 <b>{data.get('name', '—')} {data.get('surname', '')}</b>\n"
        f"🆔 ID: <code>{data.get('applicant_id', '—')}</code>\n"
        f"📞 Телефон: {data.get('phone_num', '—')}\n"
        f"🏫 Школа: {data.get('school', '—')}\n"
        f"📈 Статус: {data.get('status', '—')}\n"
        f"🔁 Попытка: {data.get('attempt', '—')}"
    )

    base64_img = data.get("base64")
    if base64_img:
        try:
            image_path = Path(f"temp_{uuid.uuid4().hex}.jpg")
            with open(image_path, "wb") as img_file:
                img_file.write(base64.b64decode(base64_img))

            photo = FSInputFile(image_path)
            await message.answer_photo(photo=photo, caption=text, parse_mode="HTML")
            image_path.unlink(missing_ok=True)
        except Exception as e:
            await message.answer(f"{text}\n\n⚠️ Ошибка при отправке фото: {e}", parse_mode="HTML")
    else:
        await message.answer(text, parse_mode="HTML")
