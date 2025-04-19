from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from tg_bot.config import bot, admin, db
from .key_boards import cancel_kb, group_kb


group_router = Router()

class Groups(StatesGroup):
    new_group = State()


@group_router.callback_query(F.data == "add_group")
async def new_group(call: types.CallbackQuery, state: FSMContext):
    if call.message.chat.id > 0 and call.from_user.id == admin:
        await state.set_state(Groups.new_group)
        await bot.send_message(call.from_user.id, "Нажмите на кнопку и выберите чат",reply_markup=group_kb)
        await bot.send_message(call.from_user.id, "Идет процесс добавления нового чата",reply_markup=cancel_kb)


@group_router.message(Groups.new_group)
async def chat_shared(message: types.Message, state: FSMContext):
    if message.chat_shared:
        if message.chat_shared.chat_id in [i[0] for i in db.get_groups()]:
            await message.answer(f"Группа с id {message.chat_shared.chat_id} уже существует")
        else:
            db.new_teacher({"tg_id": message.user_shared.user_id})
            await message.answer(f"Группа с id {message.chat_shared.chat_id} был добавлен")
        await state.clear()
    else:
        await message.answer("Отправлено сообщение не верного формата")

@group_router.callback_query(F.data == "clear_groups")
async def clear_groups(call: types.CallbackQuery):
    if call.from_user.id == admin:
        db.clear_table("groups")
        await bot.send_message(call.from_user.id, "Список групп был очищен")
