import logging
import asyncio
import re
import sys
import requests
from datetime import datetime
from aiogram import Bot, Dispatcher, types,F,html
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.enums import ParseMode
from states import Registration
from token_1 import TOKEN
from aiogram.types import CallbackQuery
from aiogram.client.default import DefaultBotProperties
from buttons import *




logging.basicConfig(level=logging.INFO)


bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await message.answer("Assalomu alaykum, hurmatli. Jalol Boltayevning onlayn kursida oʻqimoqchimisiz? Men ustoz Jalol Boltayevning yordamichi botiman! 😎🤖 Ism-familiya, telefon raqami kabi baʼzi maʼlumotlaringizni yozib olishim kerak. Bu juda qisqa vaqt oladi. Keyin sizga yopiq guruhning havolasini yuboraman.")
    await message.answer("Demak, boshladik.Iltimos, familiya-ismingizni yozing (diqqat! dastlab familiya, keyin ismingizni yozing. Masalan, Boltayev Jalol).")
    await state.set_state(Registration.surname_name)


@dp.message(Registration.surname_name)
async def process_surname_name(message: types.Message, state: FSMContext):
    full_name = message.text.strip()
    user_id = message.from_user.id
    username = message.from_user.username  # Collect username
    
    # fullname ni surname va name ga split qilish
    if " " in full_name:
        surname, name = full_name.split(maxsplit=1)

        # Uzbek familiyani tekshirish
        if re.search(r'(ov|ova|ev|eva)$', surname):
            #Lotin harflarda yozishni talab qiladi
            if re.match(r'^[A-Za-z ]+$', full_name):
                await state.update_data(surname=surname, name=name, user_id=user_id, username=username)
                
                await message.answer("Telefon raqamingizni ulashing:", reply_markup=contact)
                await state.set_state(Registration.waiting_for_phone_number)
            else:
                await message.answer("Iltimos, familiya va ismingizni faqat lotin alifbosida kiriting.")
        else:
            await message.answer("Iltimos, to'g'ri familiya va ismni kiriting.")
    else:
        await message.answer("Iltimos, familiya va ismingizni bitta xabar ichida kiriting.")




# @dp.message(Registration.waiting_for_phone_number)
# async def user_surname(message: types.Message, state: FSMContext):
#     await state.update_data(surname=message.text)
#     # await message.answer("Telefon raqamingizni ulashing:", reply_markup=contact)
#     await state.set_state(Registration.new_number)




@dp.message(F.contact,Registration.waiting_for_phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    if message.contact:
        phone_number1 = message.contact.phone_number

        if phone_number1.startswith('+998'):
            await state.update_data(phone_number=phone_number1)
            await message.answer("Sizda qoʻshimcha telefon raqami bormi? Bor boʻlsa, 972990066 koʻrinishda yozib yuboring. Agar qoʻshimcha raqam mavjud boʻlmasa, “oʻtkazib yuborish” tugmasini bosing.", reply_markup=pass_number)

            await state.set_state(Registration.new_number)
        else:
            await message.answer("Telefon raqami noto'g'ri, iltimos, +998 bilan boshlanuvchi raqamni ulashing.")
    else:
        await message.answer("Iltimos, telefon raqamingizni ulashish uchun tugmani bosing.")

# @dp.callback_query(lambda c: c.data in checkbox_options)
# async def EditBtn(call: CallbackQuery):
#     checkbox_options[call.data] = not checkbox_options[call.data]
#     await bot.edit_message_reply_markup(
#         chat_id=call.message.chat.id, 
#         message_id=call.message.message_id, 
#         reply_markup=GetCheckbox()
#     )


@dp.callback_query(F.data=="o'tkazish")
async def New_profession(callback:CallbackQuery,state:FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await state.update_data(proffession=callback)
    await callback.message.answer("Qaysi toifadansiz. Bir yoki birdan ortiq variantni tanlashingiz ham mumkin!",reply_markup=proffession)
    await state.set_state(Registration.profession_of_user) 


@dp.callback_query(Registration.profession_of_user)
async def choose_profession(callback: CallbackQuery, state: FSMContext):
    profession = callback.data

    # Define URLs for each profession
    urls = {
        'oqituvchi':   'https://t.me/+XRN0h6ghdMc4MzYy',
        'repetitor':   'https://t.me/+XRN0h6ghdMc4MzYy',
        'abituriyent': 'https://t.me/+XRN0h6ghdMc4MzYy',
        'talaba':      'https://t.me/+XRN0h6ghdMc4MzYy'
    }

    # Check if the profession is valid and send the corresponding URL
    if profession in urls:
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        chosen_url = urls[profession]
        await callback.message.answer(f"Siz tanlagan kasb: {profession}. Mana siz uchun havola: {chosen_url} ✅")
        await state.update_data(kasb=profession)  # Save profession in state
        await callback.message.answer("Iltimos, tug'ilgan sanangizni kiriting (yil-oy-kun formatida):")
        await state.set_state(Registration.birthday_date)
    else:
        await callback.message.answer("Ma'lumot yuborishda xato bor.")
        





@dp.message(Registration.birthday_date)
async def process_birthday(message: types.Message, state: FSMContext):
    birthday = message.text.strip()
    
    try:
        
        birthday_date = datetime.strptime(birthday, '%Y-%m-%d').date()
        await state.update_data(birthday=birthday_date)
        
        
        await message.answer("Yashaydigan viloyatingizni tanlang", reply_markup=provinces_of_uzb)



        await state.set_state(Registration.viloyatlar)
    except ValueError:
        await message.answer("Iltimos, tug'ilgan sanani to'g'ri formatda kiriting (yil-oy-kun).")

@dp.callback_query(F.data.startswith('province='), Registration.viloyatlar)
async def process_province(callback: CallbackQuery, state: FSMContext):
    selected_province = callback.data.split('=')[1]

    try:

        await state.update_data(viloyatlar=selected_province)
            
            
        await callback.message.answer("Ma'lumotlaringiz yuborish uchun tayyor, iltimos, tasdiqlashni bosing:", reply_markup=action_keyboard())
        await state.set_state(Registration.tasdiqlov)
    except:
        await callback.message.answer("Iltimos, viloyatni to'g'ri kiriting.")


    # await message.answer("Ma'lumotlaringiz yuborish uchun tayyor, iltimos, tasdiqlashni bosing:", reply_markup=action_keyboard())
    # await state.set_state(Registration.tasdiqlov)
# @dp.message()
# async def process_phone_number(message: types.Message, state: FSMContext):
#         user_id = message.from_user.id  
#         await state.update_data(user_id=user_id)
#         await message.answer("Ma'lumotlaringizni yuborish yoki bekor qilishni tanlang:", reply_markup=action_keyboard())
#         await state.set_state(Registration.tasdiqlov)


@dp.message(Registration.new_number)
async def process_new_number(message: types.Message, state: FSMContext):
    extra_phone_number = message.text.strip()  # Strip whitespace
    
    # Validate extra phone number
    if re.match(r'^\+998\d{9}$', extra_phone_number):
        await state.update_data(new_number=extra_phone_number)
        await state.set_state(Registration.profession_of_user)
        await message.answer("Qaysi toifadansiz. Bir yoki birdan ortiq variantni tanlashingiz ham mumkin!", reply_markup=proffession)
    else:
        await message.answer("Iltimos, telefon raqamini to'g'ri formatda kiriting (+998xxxxxxxxx).")


@dp.callback_query(F.data == "send", Registration.tasdiqlov)
async def send_data(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    name = user_data.get("name")
    surname = user_data.get("surname")
    phone_number = user_data.get("phone_number")
    user_id = user_data.get("user_id")
    username = user_data.get("username")
    extra_number = user_data.get("new_number", "qo'shimcha raqam yo'q")
    kasb = user_data.get('kasb', 'Ma\'lum emas')  # Default value if kasb is not set
    birthday = user_data.get("birthday").strftime("%Y-%m-%d") if user_data.get("birthday") else None
    viloyati = user_data.get("viloyatlar")
    
    registered_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    headers = {'Content-Type': 'application/json'}
    data1 = {
        'data': {
            'ism': name,
            'familiya': surname,
            'nomer': phone_number,
            'telegram_id': user_id,
            'username': username,
            'registratsiya_sanasi': registered_date,
            "qo'shimcha_raqam": extra_number,
            'kasb': kasb,  # Ensure profession is included here
            'tugilgan_sana': birthday,
            'viloyatlar': viloyati
        }
    }

    response = requests.post('https://sheetdb.io/api/v1/ikta4qhzjerp8', json=data1, headers=headers)

    if response.status_code == 200 or response.status_code == 201:
        await callback.message.answer("Ma'lumotlaringiz yuborildi ✅")
    else:
        await callback.message.answer("Ma'lumotlarni yuborishda xatolik yuz berdi.")

    await state.clear()



# @dp.message(Registration.viloyatlar)
# async def process_birthday(message: types.Message, state: FSMContext):
#     birthday = message.text.strip()
    
    
#     try:
#         birthday_date = datetime.strptime(birthday, '%Y-%m-%d').date()
#         await state.update_data(birthday=birthday_date)
#         await message.answer("Ma'lumotlaringiz yuborish uchun tayyor, iltimos, tasdiqlashni bosing:", reply_markup=action_keyboard())
#         await state.set_state(Registration.tasdiqlov)
#     except ValueError:
#         await message.answer("Iltimos, tug'ilgan sanani to'g'ri formatda kiriting (yil-oy-kun).")





@dp.callback_query(F.data == "o'tkazish", Registration.new_number)
async def skip_number(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await state.update_data(new_number="qo'shimcha raqam yo'q")  # No extra number provided
    await state.set_state(Registration.profession_of_user)
    await callback.message.answer("Qaysi toifadansiz. Bir yoki birdan ortiq variantni tanlashingiz ham mumkin!", reply_markup=proffession)

@dp.callback_query(F.data=="cancel", Registration.tasdiqlov )
async def cancel_data(callback:CallbackQuery, state: FSMContext):
    await callback.message.answer("Ma'lumotlaringiz bekor qilindi ❌")
    await callback.message.answer("Davom etish uchun qaytadan  /start  tugmasini bosing")
    await state.clear()



async def main() -> None:
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())