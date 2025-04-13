from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, KeyboardButtonRequestUser,
                           KeyboardButtonRequestChat,  ReplyKeyboardMarkup)


start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Проверить по ID", callback_data="id_check"),
            InlineKeyboardButton(text="Проверить по лицу", callback_data="face_check"),
        ]
    ]
)


cancel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отменить проверку", callback_data="cancel"),
        ]
    ]
)

admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Проверить по ID", callback_data="id_check"),
            InlineKeyboardButton(text="Проверить по лицу", callback_data="face_check")
        ],
        [
            InlineKeyboardButton(text="Добавить чат", callback_data="add_group"),
            InlineKeyboardButton(text="Добавить учителя", callback_data="add_teacher")
        ],
        [
            InlineKeyboardButton(text="Очистить список чатов", callback_data="clear_groups"),
            InlineKeyboardButton(text="Очистить список учителей", callback_data="clear_teachers")
        ],
        [
            InlineKeyboardButton(text="Сменить админа", callback_data="change_admin")
        ]
    ]
)



request_chat_button = KeyboardButton(
    text="Выбрать чат",
    request_chat=KeyboardButtonRequestChat(
        request_id=1,
        chat_is_channel=False,
        chat_is_forum=False,
        user_administrator_rights=None,
        bot_administrator_rights=None,
    )
)

group_kb = ReplyKeyboardMarkup(
    keyboard=[[request_chat_button]],
    resize_keyboard=True,
    one_time_keyboard=True
)

request_user_button = KeyboardButton(
    text="Выбрать пользователя",
    request_user=KeyboardButtonRequestUser(
        request_id=2,
        user_is_bot=False
    )
)

user_kb = ReplyKeyboardMarkup(
    keyboard=[[request_user_button]],
    resize_keyboard=True,
    one_time_keyboard=True
)
