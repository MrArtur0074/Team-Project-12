from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import bot, db
from .key_boards import cancel_kb, user_kb, admin_kb

teacher_router = Router()

class Teachers(StatesGroup):
    teacher_reg = State()


@teacher_router.callback_query(F.data == "cancel")
async def cancel_registration(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.clear()
    await call.message.answer("Процесс приостановлен")


@teacher_router.callback_query(F.data == "add_teacher")
async def new_teacher(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id != db.get_admin()[1]:
        await call.answer("Нет доступа", show_alert=True)
        return

    await call.message.delete()
    await state.set_state(Teachers.teacher_reg)
    await call.message.answer("Нажмите на кнопку и выберите учителя", reply_markup=user_kb)
    await call.message.answer("Идёт процесс добавления нового учителя", reply_markup=cancel_kb)


@teacher_router.message(Teachers.teacher_reg)
async def user_shared(message: types.Message, state: FSMContext):
    await message.delete()

    if not message.user_shared:
        await message.answer("Отправлено сообщение не верного формата.")
        return

    user_id = message.user_shared.user_id

    if user_id in [i[1] for i in db.get_teachers()]:
        await message.answer(f"Учитель с ID {user_id} уже существует.")
    else:
        db.new_teacher({"tg_id": user_id})
        await message.answer(f"Учитель с ID {user_id} был добавлен.")

    await state.clear()
    await message.answer(f"Здравствуйте! {message.from_user.full_name}", reply_markup=admin_kb)


@teacher_router.callback_query(F.data == "clear_teachers")
async def clear_teachers(call: types.CallbackQuery):
    if call.from_user.id != db.get_admin()[1]:
        await call.answer("Нет доступа", show_alert=True)
        return

    await call.message.delete()
    db.clear_table("teachers")
    db.new_teacher({"tg_id": db.get_admin()[1]})
    await call.message.answer("Список учителей был очищен.")
    await call.message.answer(f"Здравствуйте! {call.from_user.full_name}", reply_markup=admin_kb)
