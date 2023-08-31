from aiogram import F, Router
from aiogram.filters import Command

from src.dialogs.commands import start_command
from src.dialogs.main_menu import get_dialog as get_main_menu_dialog
from src.dialogs.registration import get_dialog as get_registration_dialog
from src.dialogs.report_generator import get_dialog as get_report_dialog
from src.dialogs.settings_menu import get_dialog as get_settings_dialog
from src.dialogs.weekend import get_dialog as get_weekend_dialog
from src.ui_commands import Commands


def register_dialogs(router: Router) -> None:
    dialog_router = Router()
    registration_dialog = get_registration_dialog()
    main_menu_dialog = get_main_menu_dialog()
    settings_dialog = get_settings_dialog()
    weekend_dialog = get_weekend_dialog()
    report_dialog = get_report_dialog()
    dialog_router.include_router(registration_dialog)
    dialog_router.include_router(main_menu_dialog)
    dialog_router.include_router(settings_dialog)
    dialog_router.include_router(weekend_dialog)
    dialog_router.include_router(report_dialog)

    dialog_router.message(Command(Commands.START))(start_command)

    router.message.filter(F.chat.type == "private")
    router.include_router(dialog_router)
