from telegram import Update
from telegram.ext import ContextTypes
from src.handlers.base_handler import BaseHandler
from src.database.training_state import TrainingState
from src.utils.enum_exercise_type import ExerciseType


class Start(BaseHandler):

    questions_step_1 = {}
    questions_step_2 = {}
    questions_step_3 = {}
    questions_step_4 = {}

    @classmethod
    async def init(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        training_model = TrainingState()
        training_model.connect()

        training_words = training_model.get_vocabs_to_training()
        for line in training_words:
            vocab_id = line.get('vocab_id')
            streak = line.get('streak')
            exercise_type = ExerciseType.get_exercise_by_streak(streak)

            if exercise_type == ExerciseType.EN_TRANSLATION:
                cls.questions_step_1[vocab_id] = {
                    'question': f"Qual a tradução da palavra/expressão '<strong>{line.get('word').upper()}</strong>' para português?",
                    'correct_response': line.get('meaning'),
                    'options': []
                }
            elif exercise_type == ExerciseType.PT_TRANSLATION:
                cls.questions_step_1[vocab_id] = {
                    'question': f"Qual a tradução da palavra/expressão '<strong>{line.get('meaning').upper()}</strong>' para inglês?",
                    'correct_response': line.get('word'),
                    'options': []
                }
            else:
                continue

        print('\nNIVEL 1')
        for _, line in cls.questions_step_1.items():
            print(line)

        print('\nNIVEL 2')
        for _, line in cls.questions_step_2.items():
            print(line)

        print('\nNIVEL 3')
        for _, line in cls.questions_step_3.items():
            print(line)

        print('\nNIVEL 4')
        for _, line in cls.questions_step_4.items():
            print(line)