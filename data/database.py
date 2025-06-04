import aiosqlite

DB_NAME = 'quiz_bot.db'


async def create_tables():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state 
                          (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS user_stats 
                          (user_id INTEGER PRIMARY KEY, username TEXT, 
                          last_score INTEGER, total_answers INTEGER, 
                          correct_answers INTEGER)''')
        await db.commit()


async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)',
                         (user_id, index))
        await db.commit()


async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0


async def update_user_stats(user_id, username, is_correct):
    async with aiosqlite.connect(DB_NAME) as db:
        # Получаем текущую статистику
        async with db.execute('''SELECT total_answers, correct_answers 
                               FROM user_stats WHERE user_id = ?''', (user_id,)) as cursor:
            stats = await cursor.fetchone()

        total = 1 if not stats else stats[0] + 1
        correct = (1 if is_correct else 0) if not stats else stats[1] + (1 if is_correct else 0)

        await db.execute('''INSERT OR REPLACE INTO user_stats 
                          (user_id, username, last_score, total_answers, correct_answers) 
                          VALUES (?, ?, ?, ?, ?)''',
                         (user_id, username, correct, total, correct))
        await db.commit()


async def get_user_stats(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('''SELECT last_score, total_answers, correct_answers 
                               FROM user_stats WHERE user_id = ?''', (user_id,)) as cursor:
            return await cursor.fetchone()


async def get_leaderboard():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('''SELECT username, last_score, correct_answers, total_answers 
                               FROM user_stats ORDER BY last_score DESC LIMIT 10''') as cursor:
            return await cursor.fetchall()
        