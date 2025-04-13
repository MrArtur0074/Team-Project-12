from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from tg_bot.config import bot, admin, db, teachers
from .key_boards import cancel_kb, user_kb


teacher_router = Router()

class Teachers(StatesGroup):
    teacher_reg = State()


@teacher_router.callback_query(F.data == "add_teacher")
async def new_teacher(call: types.CallbackQuery, state: FSMContext):
    if call.message.chat.id > 0 and call.from_user.id == admin:
        await state.set_state(Teachers.teacher_reg)
        await bot.send_message(call.from_user.id, "Нажмите на кнопку и выберите учиетля",reply_markup=user_kb)
        await bot.send_message(call.from_user.id, "Идет процесс добавления нового учителя",reply_markup=cancel_kb)


@teacher_router.message(Teachers.teacher_reg)
async def user_shared(message: types.Message, state: FSMContext):
    if message.user_shared:
        if message.user_shared.user_id in teachers:
            await message.answer(f"Учитель с id {message.user_shared.user_id} уже существует")
        else:
            # todo
            # create object in DB
            await message.answer(f"Учитель с id {message.user_shared.user_id} был добавлен")
        await state.clear()
    else:
        await message.answer("Отправлено сообщение не верного формата")

@teacher_router.callback_query(F.data == "clear_teachers")
async def clear_teachers(call: types.CallbackQuery):
    if call.from_user.id == admin:
        # todo
        # clear db
        await bot.send_message(call.from_user.id, "Нажмите на кнопку и выберите учиетля")
