import sys
import time
import random
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
from src.utils.decorator_auth import only_authorized


class Start(BaseHandler):

    questions_step_1 = []
    questions_step_2 = []
    questions_step_3 = []
    questions_step_4 = []
    current_question: Question = None
    current_questions = []
    current_level = None
    correct_responses = []
    wrong_responses = []
    total_questions = 0
    total_responses = 0

    @classmethod
    @only_authorized
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
                word = str(line.get('word')).upper()
                streak = line.get('streak')
                exercise_type = ExerciseType.get_exercise_by_streak(streak)

                if exercise_type == ExerciseType.EN_TRANSLATION:
                    cls.questions_step_1.append(Question(
                        vocab_id=vocab_id,
                        question=f"Qual a tradução da palavra/expressão '<strong>{line.get('word').upper()}</strong>' para português?",
                        correct_response=line.get('meaning'),
                        options=get_random_itens(portuguese_words, 3, word=line.get('meaning'))
                    ))
                elif exercise_type == ExerciseType.PT_TRANSLATION:
                    cls.questions_step_1.append(Question(
                        vocab_id=vocab_id,
                        question=f"Qual a tradução da palavra/expressão '<strong>{line.get('meaning').upper()}</strong>' para inglês?",
                        correct_response=line.get('word'),
                        options=get_random_itens(english_words, 3, word=line.get('word'))
                    ))
                elif exercise_type == ExerciseType.CLOZE_WITH_HINT_AND_FIRST_WORD:
                    for sentence in get_random_itens(sentences.get(vocab_id, []), 1):
                        cls.questions_step_2.append(Question(
                            vocab_id=vocab_id,
                            question=sentence,
                            correct_response=word,
                            hint=line.get('hint'),
                            first_word=True
                        ))
                elif exercise_type == ExerciseType.CLOZE_WITH_HINT:
                    for sentence in get_random_itens(sentences.get(vocab_id, []), 1):
                        cls.questions_step_2.append(Question(
                            vocab_id=vocab_id,
                            question=sentence,
                            correct_response=word,
                            hint=line.get('hint')
                        ))
                elif exercise_type == ExerciseType.CLOZE_WITHOUT_HINT:
                    for sentence in get_random_itens(sentences.get(vocab_id, []), 1):
                        cls.questions_step_3.append(Question(
                            vocab_id=vocab_id,
                            question=sentence,
                            correct_response=word
                        ))
                elif exercise_type == ExerciseType.LEARNEAD:
                    for sentence in get_random_itens(sentences.get(vocab_id, []), 1):
                        cls.questions_step_4.append(Question(
                            vocab_id=vocab_id,
                            question=sentence,
                            correct_response=word
                        ))
                else:
                    continue

            random.shuffle(cls.questions_step_1)
            random.shuffle(cls.questions_step_2)
            random.shuffle(cls.questions_step_3)
            random.shuffle(cls.questions_step_4)

            TimeQuestions.start_questions()
            if cls.questions_step_1:
                cls.current_level = 1
                cls.current_questions = cls.questions_step_1.copy()
            elif cls.questions_step_2:
                cls.current_level = 2
                cls.current_questions = cls.questions_step_2.copy()
            elif cls.questions_step_3:
                cls.current_level = 3
                cls.current_questions = cls.questions_step_3.copy()
            elif cls.questions_step_4:
                cls.current_level = 4
                cls.current_questions = cls.questions_step_4.copy()

            cls.total_questions = len(cls.questions_step_1) + len(cls.questions_step_2) + len(cls.questions_step_3) + len(cls.questions_step_4)
            await cls.send_question(update, context, cls.current_questions, cls.handle_questions_user)
        except Exception as error:
            await cls.send_error(update, context, error, sys.exc_info())

    @classmethod
    async def handle_questions_user(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, response: str):
        try:
            if TimeQuestions.is_finished():
                await cls.finish(update, context, 'Tempo esgotado, voltamos a nos falar amanhã ;)')
                await cls.save_score(update, context)
                context.application.stop_running()
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

            if cls.current_question.get_response().upper() == response.upper():
                await cls.mark_response(update, context, True, cls.current_question.get_response().upper())
                cls.correct_responses.append(cls.current_question.get_vocab_id())
            else:
                await cls.mark_response(update, context, False, cls.current_question.get_response().upper())
                cls.wrong_responses.append(cls.current_question.get_vocab_id())

            if len(cls.current_questions) == 0:
                await cls.save_score(update, context)
            elif (len(cls.correct_responses) + len(cls.wrong_responses)) >= 5:
                await cls.save_score(update, context)

            if cls.total_questions == cls.total_responses:
                await cls.finish(update, context, 'Quiz finalizou, voltamos a nos falar amanhã ;)')
                context.application.stop_running()
                return

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

    @classmethod
    async def save_score(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            training_model = TrainingState()
            training_model.connect()
            vocabs_score = training_model.get_vocabs_score()

            increase_confidence = []
            increase_streak = []
            decrease_confidence = []
            decrease_streak = []
            update_last_review = []

            for vocab_id in cls.correct_responses:
                aux_vocab = vocabs_score.get(vocab_id)
                if int(aux_vocab.get('confidence')) < 2:
                    increase_confidence.append(str(vocab_id))
                else:
                    if int(aux_vocab.get('streak')) < 5:
                        increase_streak.append(str(vocab_id))
                    else:
                        update_last_review.append(str(vocab_id))

            for vocab_id in cls.wrong_responses:
                aux_vocab = vocabs_score.get(vocab_id)
                if int(aux_vocab.get('confidence')) == 0:
                    if int(aux_vocab.get('streak')) > 0:
                        decrease_streak.append(str(vocab_id))
                    else:
                        update_last_review.append(str(vocab_id))
                else:
                    decrease_confidence.append(str(vocab_id))

            count = 0
            while count < 5:
                count += 1
                try:
                    training_model.change_confidence(increase_confidence, increase=True)
                    training_model.change_confidence(decrease_confidence, decrease=True)

                    training_model.change_streak(increase_streak, increase=True)
                    training_model.change_streak(decrease_streak, decrease=True)

                    training_model.update_last_review(update_last_review)
                    await cls.send_message(update, context, 'SALVOU TUDO!')
                    break
                except Exception as error:
                    await cls.send_error(update, context, error, sys.exc_info())
                    time.sleep(60)
                    training_model = TrainingState()
                    training_model.connect()

                time.sleep(60)

            cls.total_responses += len(cls.correct_responses)
            cls.total_responses += len(cls.wrong_responses)

            cls.correct_responses.clear()
            cls.wrong_responses.clear()
        except Exception as error:
            await cls.send_error(update, context, error, sys.exc_info())
