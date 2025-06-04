from aiogram import types
from data.quiz_data import quiz_data
from keyboards.builders import generate_options_keyboard
from data.database import update_quiz_index, get_quiz_index, update_user_stats, get_user_stats


async def get_question(message: types.Message, user_id: int):
    current_question_index = await get_quiz_index(user_id)
    question_data = quiz_data[current_question_index]

    await message.answer(
        f"Вопрос {current_question_index + 1}/{len(quiz_data)}:\n{question_data['question']}",
        reply_markup=generate_options_keyboard(
            question_data['options'],
            question_data['options'][question_data['correct_option']]
        )
    )


async def new_quiz(message: types.Message):
    print(f"DEBUG: New quiz started by {message.from_user.id}")
    user_id = message.from_user.id
    await update_quiz_index(user_id, 0)
    await get_question(message, user_id)


async def right_answer(callback: types.CallbackQuery):
    await handle_answer(callback, is_correct=True)


async def wrong_answer(callback: types.CallbackQuery):
    await handle_answer(callback, is_correct=False)


async def handle_answer(callback: types.CallbackQuery, is_correct: bool):
    user = callback.from_user
    await callback.bot.edit_message_reply_markup(
        chat_id=user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(user.id)
    question_data = quiz_data[current_question_index]

    if is_correct:
        await callback.message.answer("✅ Верно!")
    else:
        correct_option = question_data['options'][question_data['correct_option']]
        await callback.message.answer(
            f"❌ Неверно! Правильный ответ: {correct_option}\n\n{question_data['explanation']}")

    await update_user_stats(user.id, user.username, is_correct)
    await update_quiz_index(user.id, current_question_index + 1)

    if current_question_index + 1 < len(quiz_data):
        await get_question(callback.message, user.id)
    else:
        stats = await get_user_stats(user.id)
        await callback.message.answer(
            f"🎉 Квиз завершен!\n"
            f"Ваш результат: {stats[0]}/{len(quiz_data)}\n"
            f"Общая статистика: {stats[1]}/{stats[2]} правильных ответов"
        )
        