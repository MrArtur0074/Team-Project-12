from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from tg_bot.config import teachers, bot
from .key_boards import cancel_kb


fsm_router = Router()

class FaceIDCheck(StatesGroup):
    face = State()
    id = State()


@fsm_router.message(F.data == "cancel")
async def cancel_registration(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await bot.send_message(call.from_user.id, "Проверка отменена")


@fsm_router.callback_query(F.data == "face_check")
async def face_check(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id in teachers and call.message.chat.id > 0:
        await state.set_state(FaceIDCheck.face)
        await bot.send_message(call.from_user.id, "Отправьте лицо студента", reply_markup=cancel_kb)


@fsm_router.message(FaceIDCheck.face)
async def face_response(message: types.Message, state: FSMContext):
    # todo
    # send request and get response
    await state.clear()
    await message.answer("Ответ от сервера...")


@fsm_router.callback_query(F.data == "id_check")
async def id_check(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id in teachers and call.message.chat.id > 0:
        await state.set_state(FaceIDCheck.id)
        await bot.send_message(call.from_user.id, "Напишите id студента", reply_markup=cancel_kb)


@fsm_router.message(FaceIDCheck.id)
async def id_response(message: types.Message, state: FSMContext):
    # todo
    # send request and get response
    await state.clear()
    await message.answer("Ответ от сервера...")
