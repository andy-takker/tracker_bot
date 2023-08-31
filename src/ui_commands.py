from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


class Commands:
    START = "start"
    MENU = "menu"
    REPORT = "report"


async def set_ui_commands(bot: Bot) -> None:
    """Set bot commands in UI."""
    commands = [
        BotCommand(command=Commands.START, description="Начать работу c ботом"),
        BotCommand(command=Commands.MENU, description="Открыть меню"),
        BotCommand(command=Commands.REPORT, description="Сформировать отчет"),
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats(),
    )
