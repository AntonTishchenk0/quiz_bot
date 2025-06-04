from aiogram import types
from aiogram.filters.command import Command
from keyboards.builders import create_main_keyboard


async def cmd_start(message: types.Message):
    kb = create_main_keyboard()
    await message.answer(
        "Добро пожаловать в квиз по Python!\n"
        "Выберите действие:",
        reply_markup=kb
    )


async def cmd_help(message: types.Message):
    help_text = (
        "📚 Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/quiz - Начать новую викторину\n"
        "/stats - Показать вашу статистику\n"
        "/leaderboard - Показать таблицу лидеров\n\n"
        "Используйте кнопки меню для удобной навигации!"
    )
    await message.answer(help_text)


async def handle_unknown_message(message: types.Message):
    await message.answer("Извините, я не понимаю эту команду. Попробуйте /help для списка доступных команд.")
