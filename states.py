from aiogram.fsm.state import StatesGroup, State

class Registration(StatesGroup):
    # surname = State()
    # name = State()
    surname_name=State()
    waiting_for_phone_number=State()
    new_number=State()
    profession_of_user=State()
    birthday_date=State()
    viloyatlar=State()
    tasdiqlov=State()
    
