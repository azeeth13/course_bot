# from main1 import *

import re
# def ResponseFunc():
def t_check(a):
    ok = "^[+]998([0-9][012345789]|[0-9][125679]|7[01234569])[0-9]{7}$"
    ok1 = "^998([0-9][012345789]|[0-9][125679]|7[01234569])[0-9]{7}$"

    if re.match(ok, a) or re.match(ok1, a):
        return True
    else:
        return False
    






# @dp.message(Command('/1'))
# async def first_command(message:types.Message):
#     await message.answer('https://t.me/walpapersUz')


# @dp.message(Command('/2'))
# async def second_command(message:types.Message):
#     await message.answer("https://t.me/lollifamily")


# @dp.message(Command('/3'))
# async def third_command(message:types.Message):
#     await message.answer("https://t.me/bangtan7_new")

# @dp.message(Command('/4'))
# async def fourth_command(message:types.Message):
#     await message.answer('https://t.me/temki_77',str("Talabalar uchun"))
