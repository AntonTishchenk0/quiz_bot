from typing import Optional


class UserStats:
    def __init__(self, user_id: int, username: str, last_score: int, total_answers: int, correct_answers: int):
        self.user_id = user_id
        self.username = username
        self.last_score = last_score
        self.total_answers = total_answers
        self.correct_answers = correct_answers


class QuizQuestion:
    def __init__(self, question: str, options: list[str], correct_option: int, explanation: str):
        self.question = question
        self.options = options
        self.correct_option = correct_option
        self.explanation = explanation
