from aiogram.fsm.state import State, StatesGroup


class AddCategory(StatesGroup):
    waiting_name = State()


class AddVideo(StatesGroup):
    choosing_category = State()
    waiting_video = State()
    waiting_title = State()
    waiting_description = State()


class EditVideo(StatesGroup):
    waiting_new_title = State()
    waiting_new_description = State()
    waiting_new_file = State()
