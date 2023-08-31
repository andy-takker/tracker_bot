from aiogram.fsm.state import State, StatesGroup


class SetTimeSG(StatesGroup):
    hours = State()
    minutes = State()


class RegistrationSG(StatesGroup):
    set_frequency = State()
    set_time_zone = State()
    set_start_time = State()
    set_end_time = State()
    confirm = State()


class MainMenuSG(StatesGroup):
    main_menu = State()


class ReportGenerateSG(StatesGroup):
    choose_period = State()


class WeekendSG(StatesGroup):
    change_status = State()


class SettingsSG(StatesGroup):
    menu = State()
    change_frequency = State()
    change_time_zone = State()
    change_start_time = State()
    change_end_time = State()
