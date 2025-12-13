import sys
from telegram import Update
from telegram.ext import ContextTypes
from src.handlers.base_handler import BaseHandler
from src.database.training_state import TrainingState
from src.database.vocabulary import Vocabulary
from src.database.example_sentence import ExampleSentence
from src.utils.enum_exercise_type import ExerciseType
from src.utils.functions import get_random_itens
from src.controllers.question import Question
from src.controllers.time_questions import TimeQuestions


class Start(BaseHandler):

    questions_step_1 = []
    questions_step_2 = []
    questions_step_3 = []
    questions_step_4 = []
    current_question = None
    current_questions = []
    current_level = None
    last_question = False
    response_last_question = False

    @classmethod
    async def init(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            vocabulary_model = Vocabulary()
            vocabulary_model.connect()

            training_model = TrainingState()
            training_model.connect()

            sentence_model = ExampleSentence()
            sentence_model.connect()

            english_words = vocabulary_model.get_all_english_words()
            portuguese_words = vocabulary_model.get_all_portuguese_words()

            vocabs_to_learn = []
            training_words = training_model.get_vocabs_to_training()
            for line in training_words:
                vocabs_to_learn.append(line.get('vocab_id'))

            sentences = sentence_model.get_sentences_by_vocab(vocabs_to_learn)

            for line in training_words:
                vocab_id = line.get('vocab_id')
                word = line.get('word')
                streak = line.get('streak')
                exercise_type = ExerciseType.get_exercise_by_streak(streak)

                if exercise_type == ExerciseType.EN_TRANSLATION:
                    cls.questions_step_1.append(Question(
                        question=f"Qual a tradução da palavra/expressão '<strong>{line.get('word').upper()}</strong>' para português?",
                        correct_response=line.get('meaning'),
                        options=get_random_itens(line.get('meaning'), portuguese_words, 3)
                    ))
                elif exercise_type == ExerciseType.PT_TRANSLATION:
                    cls.questions_step_1.append(Question(
                        question=f"Qual a tradução da palavra/expressão '<strong>{line.get('meaning').upper()}</strong>' para inglês?",
                        correct_response=line.get('word'),
                        options=get_random_itens(line.get('word'), english_words, 3)
                    ))
                elif exercise_type == ExerciseType.CLOZE_WITH_HINT_AND_FIRST_WORD:
                    for sentence in sentences.get(vocab_id, [])[:1]:
                        question_sentence = str(sentence).replace(word, f'{word[0]}' + '_' * (len(word) -1))
                        cls.questions_step_2.append(Question(
                            question=question_sentence,
                            correct_response=word,
                            hint=line.get('hint')
                        ))
                elif exercise_type == ExerciseType.CLOZE_WITH_HINT:
                    for sentence in sentences.get(vocab_id, [])[:1]:
                        question_sentence = str(sentence).replace(word, '_' * len(word))
                        cls.questions_step_2.append(Question(
                            question=question_sentence,
                            correct_response=word,
                            hint=line.get('hint')
                        ))
                elif exercise_type == ExerciseType.CLOZE_WITHOUT_HINT:
                    for sentence in sentences.get(vocab_id, [])[:1]:
                        question_sentence = str(sentence).replace(word, '_' * len(word))
                        cls.questions_step_3.append(Question(
                            question=question_sentence,
                            correct_response=word
                        ))
                elif exercise_type == ExerciseType.LEARNEAD:
                    for sentence in sentences.get(vocab_id, [])[:1]:
                        question_sentence = str(sentence).replace(word, '_' * len(word))
                        cls.questions_step_4.append(Question(
                            question=question_sentence,
                            correct_response=word
                        ))
                else:
                    continue

            TimeQuestions.start_questions()
            cls.current_level = 1
            cls.current_questions = cls.questions_step_1.copy()
            await cls.send_question(update, context, cls.current_questions, cls.handle_questions_user)
        except Exception as error:
            await cls.send_error(update, context, error, sys.exc_info())

    @classmethod
    async def handle_questions_user(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, response: str):
        try:
            if TimeQuestions.is_finished():
                await cls.finish(update, context, 'Tempo esgotado, voltamos a nos falar amanhã ;)')
                return

            if TimeQuestions.change_level() or len(cls.current_questions) == 0:
                if cls.current_level == 1:
                    cls.current_level = 2
                    cls.current_questions = cls.questions_step_2.copy()
                elif cls.current_level == 2:
                    cls.current_level = 3
                    cls.current_questions = cls.questions_step_3.copy()
                elif cls.current_level == 3:
                    cls.current_level = 4
                    cls.current_questions = cls.questions_step_4.copy()
                elif cls.current_level == 4:
                    await cls.finish(update, context, 'As perguntas terminaram, voltamos a nos falar amanhã ;)')
                    if not cls.last_question:
                        cls.last_question = True

            if cls.last_question and not cls.last_question:
                return

            print(f'pergunta: {cls.current_question}')
            print(f'respondido: {response}')
            await cls.send_question(update, context, cls.current_questions, cls.handle_questions_user)
        except Exception as error:
            await cls.send_error(update, context, error, sys.exc_info())

    @classmethod
    async def send_question(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, questions: list, callback_func):
        try:
            if len(questions) > 0:
                question_obj: Question = questions[0]
                cls.current_question = question_obj
                questions.pop(0)

                options = question_obj.get_options()
                hint= question_obj.get_hint()
                if options:
                    options.append(question_obj.get_response())
                    await cls.ask_with_options(update, context, question_obj.get_question(), options, callback_func)
                elif hint:
                    message = question_obj.get_question()
                    message += f'\n\n<strong>HINT:</strong> <em>{hint}</em>'
                    await cls.question_message(update, context, message, callback_func)
                else:
                    await cls.question_message(update, context, question_obj.get_question(), callback_func)
        except Exception as error:
            await cls.send_error(update, context, error, sys.exc_info())