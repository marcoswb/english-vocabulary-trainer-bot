from telegram import Update
from telegram.ext import ContextTypes
from src.handlers.base_handler import BaseHandler
from src.database.training_state import TrainingState
from src.database.vocabulary import Vocabulary
from src.database.example_sentence import ExampleSentence
from src.utils.enum_exercise_type import ExerciseType
from src.utils.functions import get_random_itens


class Start(BaseHandler):

    questions_step_1 = []
    questions_step_2 = []
    questions_step_3 = []
    questions_step_4 = []

    @classmethod
    async def init(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
                cls.questions_step_1.append({
                    'question': f"Qual a tradução da palavra/expressão '<strong>{line.get('word').upper()}</strong>' para português?",
                    'correct_response': line.get('meaning'),
                    'options': get_random_itens(portuguese_words, 3)
                })
            elif exercise_type == ExerciseType.PT_TRANSLATION:
                cls.questions_step_1.append({
                    'question': f"Qual a tradução da palavra/expressão '<strong>{line.get('meaning').upper()}</strong>' para inglês?",
                    'correct_response': line.get('word'),
                    'options': get_random_itens(english_words, 3)
                })
            elif exercise_type == ExerciseType.CLOZE_WITH_HINT_AND_FIRST_WORD:
                for sentence in sentences.get(vocab_id):
                    question_sentence = str(sentence).replace(word, f'{word[0]}' + '_' * (len(word) -1))
                    cls.questions_step_2.append({
                        'question': question_sentence,
                        'correct_response': sentence,
                        'hint': line.get('hint')
                    })
            elif exercise_type == ExerciseType.CLOZE_WITH_HINT:
                for sentence in sentences.get(vocab_id):
                    question_sentence = str(sentence).replace(word, '_' * len(word))
                    cls.questions_step_2.append({
                        'question': question_sentence,
                        'correct_response': sentence,
                        'hint': line.get('hint')
                    })
            else:
                continue

        print('\nNIVEL 1')
        for line in cls.questions_step_1:
            print(line)

        print('\nNIVEL 2')
        for line in cls.questions_step_2:
            print(line)

        print('\nNIVEL 3')
        for line in cls.questions_step_3:
            print(line)

        print('\nNIVEL 4')
        for line in cls.questions_step_4:
            print(line)