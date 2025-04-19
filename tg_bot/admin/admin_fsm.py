from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from tg_bot.config import bot, admin, db
from .key_boards import cancel_kb, user_kb


admin_fsm_router = Router()

class Teachers(StatesGroup):
    teacher_reg = State()


@admin_fsm_router.callback_query(F.data == "change_admin")
async def new_teacher(call: types.CallbackQuery, state: FSMContext):
    if call.message.chat.id > 0 and call.from_user.id == admin:
        await state.set_state(Teachers.teacher_reg)
        await bot.send_message(call.from_user.id, "Нажмите на кнопку и выберите нового админа",reply_markup=user_kb)
        await bot.send_message(call.from_user.id, "Идет процесс смены админа",reply_markup=cancel_kb)


@admin_fsm_router.message(Teachers.teacher_reg)
async def user_shared(message: types.Message, state: FSMContext):
    if message.user_shared:
        if message.user_shared.user_id in [i[1] for i in db.get_teachers()]:
            await message.answer(f"Учитель с id {message.user_shared.user_id} уже существует")
        else:
            db.new_teacher({"tg_id": message.user_shared.user_id})
            await message.answer(f"Учитель с id {message.user_shared.user_id} был добавлен")
        await state.clear()
    else:
        await message.answer("Отправлено сообщение не верного формата")