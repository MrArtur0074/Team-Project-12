from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import bot, db
from key_boards import cancel_kb, user_kb, admin_kb

admin_fsm_router = Router()


class Teachers(StatesGroup):
    teacher_reg = State()


@admin_fsm_router.callback_query(F.data == "cancel")
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.clear()
    await bot.send_message(call.from_user.id, "Процесс приостановлен")


@admin_fsm_router.callback_query(F.data == "change_admin")
async def change_admin(call: types.CallbackQuery, state: FSMContext):
    admin_data = db.get_admin()
    if not admin_data or call.from_user.id != admin_data[1]:
        await call.answer("У вас нет прав для выполнения этого действия", show_alert=True)
        return

    await call.message.delete()
    await state.set_state(Teachers.teacher_reg)
    await bot.send_message(call.from_user.id, "Нажмите на кнопку и выберите нового админа", reply_markup=user_kb)
    await bot.send_message(call.from_user.id, "Идет процесс смены админа", reply_markup=cancel_kb)


@admin_fsm_router.message(Teachers.teacher_reg)
async def user_shared(message: types.Message, state: FSMContext):
    admin_data = db.get_admin()
    if not admin_data or message.from_user.id != admin_data[1]:
        await message.answer("У вас нет прав для выполнения этого действия")
        return

    await message.delete()

    if not message.user_shared:
        await message.answer("Отправлено сообщение неверного формата")
        return

    new_admin_id = message.user_shared.user_id

    db.set_admin({"admin_id": new_admin_id})
    await message.answer(f"✅ Админ с ID {new_admin_id} был успешно назначен!")

    await state.clear()

    await message.answer(
        f"Здравствуйте! {message.from_user.full_name}",
        reply_markup=admin_kb
    )
