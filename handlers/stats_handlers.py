from aiogram import types
from data.database import get_user_stats, get_leaderboard


async def show_stats(message: types.Message):
    stats = await get_user_stats(message.from_user.id)
    if stats:
        await message.answer(
            f"📊 Ваша статистика:\n"
            f"Последний результат: {stats[0]}\n"
            f"Всего ответов: {stats[2]}/{stats[1]} (правильных/всего)"
        )
    else:
        await message.answer("Вы еще не проходили квиз. Начните игру командой /quiz")


async def show_leaderboard(message: types.Message):
    leaderboard = await get_leaderboard()
    if not leaderboard:
        await message.answer("Таблица лидеров пока пуста.")
        return

    leaderboard_text = "🏆 Топ 10 игроков:\n\n"
    for i, (username, last_score, correct, total) in enumerate(leaderboard, 1):
        leaderboard_text += (
            f"{i}. {username}: {last_score} (всего {correct}/{total})\n"
        )

    await message.answer(leaderboard_text)
    