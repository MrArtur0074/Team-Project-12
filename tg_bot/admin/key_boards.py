from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



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
            InlineKeyboardButton(text="Проверить по лицу", callback_data="face_check"),
        ],
        [
            InlineKeyboardButton(text="Список всех учителей", callback_data="all_teachers"),
            InlineKeyboardButton(text="Добавить учителя", callback_data="add_teacher"),
        ],
        [
            InlineKeyboardButton(text="Список всех чатов", callback_data="all_groups"),
            InlineKeyboardButton(text="Добавить чат", callback_data="add_group"),
        ],
        [
            InlineKeyboardButton(text="Сменить админа", callback_data="change_admin"),
        ]
    ]
)