import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from handlers import commands, quiz_handlers, stats_handlers
from data.database import create_tables

logging.basicConfig(level=logging.INFO)
API_TOKEN = 'Ваш токен'


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    await create_tables()

    # Регистрация команд
    dp.message.register(commands.cmd_start, Command("start"))
    dp.message.register(commands.cmd_help, Command("help"))
    dp.message.register(quiz_handlers.new_quiz, Command("quiz"))
    dp.message.register(stats_handlers.show_stats, Command("stats"))
    dp.message.register(stats_handlers.show_leaderboard, Command("leaderboard"))

    # Регистрация обработчиков кнопок
    dp.message.register(quiz_handlers.new_quiz, F.text.in_(["Начать игру", "🎮 Начать игру"]))
    dp.message.register(stats_handlers.show_stats, F.text.in_(["Моя статистика", "📊 Моя статистика"]))
    dp.message.register(stats_handlers.show_leaderboard, F.text.in_(["Таблица лидеров", "🏆 Таблица лидеров"]))
    dp.message.register(commands.cmd_help, F.text.in_(["Помощь", "ℹ️ Помощь"]))

    # Обработчики ответов на вопросы
    dp.callback_query.register(quiz_handlers.right_answer, F.data == "right_answer")
    dp.callback_query.register(quiz_handlers.wrong_answer, F.data == "wrong_answer")

    # Обработчик для любых других сообщений
    dp.message.register(commands.handle_unknown_message)

    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
    
    
