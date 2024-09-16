from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
import requests



contact = ReplyKeyboardMarkup(
  keyboard=[
    [KeyboardButton(text='📲 Telefon raqamni yuborish', request_contact=True)]
  ],
  resize_keyboard=True, one_time_keyboard=True
)



pass_number=InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="O'tkazib yuborish",callback_data="o'tkazish")],
    ]
)

proffession=InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="O'qituvchi 👩‍🏫",callback_data='oqituvchi'),InlineKeyboardButton(text='Repetitor 🧑‍🏫',callback_data='repetitor')],
        [InlineKeyboardButton(text="Abituriyent 👩‍🎓",callback_data='abituriyent'),InlineKeyboardButton(text="Talaba 👨‍🎓",callback_data='talaba')],
    ]
)



provinces_of_uzb=InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Toshkent viloyati",callback_data='province=toshkent'),InlineKeyboardButton(text="Andijon viloyati",callback_data='province=andijon')],
        [InlineKeyboardButton(text="Buxoro viloyati",callback_data="province=buxoro"),InlineKeyboardButton(text="Fargʻona viloyati",callback_data="province=fargona")],
        [InlineKeyboardButton(text="Jizzax viloyati",callback_data='province=jizzah'),InlineKeyboardButton(text="Xorazm viloyati",callback_data='province=xorazm')],
        [InlineKeyboardButton(text="Namangan viloyati",callback_data='province=namangan'),InlineKeyboardButton(text='Navoiy viloyati',callback_data='province=navoiy')],
        [InlineKeyboardButton(text='Qashqadaryo viloyati',callback_data='province=qashaqadaryo'),InlineKeyboardButton(text="Surxondaryo viloyati",callback_data="province=surxondaryo")],
        [InlineKeyboardButton(text="Samarqand viloyati",callback_data='province=samarqand'),InlineKeyboardButton(text="Sirdaryo viloyati",callback_data='province=sirdaryo')],
        
    ]
)



# group_onetime_url={
#     [1]={""}
# }


# checkbox_options = {
#     'oqituvchi': False,
#     'repetitor': False,
#     'abituriyent': False,
#     'talaba': False
# }


# def GetCheckbox():
#     keyboard = InlineKeyboardBuilder()
#     for option, is_selected in checkbox_options.items():
#         text = f"{option} {'☑️' if is_selected else ''}"
#         keyboard.add(InlineKeyboardButton(text=text, callback_data=option))
#     keyboard.add(InlineKeyboardButton(text="✅ Yuborish", callback_data="submit"))
#     keyboard.adjust(2)
#     return keyboard.as_markup()


def action_keyboard():
    # Create the inline keyboard markup
    keyboard = InlineKeyboardBuilder()  # Adjust row_width if needed
    # Add buttons to the keyboard
    keyboard.add(
        InlineKeyboardButton(text="Yuborish", callback_data="send"),
    )
    keyboard.add(
        InlineKeyboardButton(text="Bekor qilish", callback_data="cancel")
    )
    keyboard.adjust(1)
    return keyboard.as_markup()