import sys
from telegram import Update
from telegram.ext import ContextTypes
from src.handlers.base_handler import BaseHandler
from src.database.vocabulary import Vocabulary
from src.database.example_sentence import ExampleSentence
from src.database.training_state import TrainingState
from src.database.candidate_words import CandidateWords
from src.utils.decorator_auth import only_authorized
from src.utils.functions import get_meaning_data_api, get_complement_data_llm

class AddVocab(BaseHandler):

    current_index = 0
    words_to_process = []
    candidate_words = CandidateWords()

    @classmethod
    @only_authorized
    async def init(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            cls.candidate_words.connect()

            words = cls.candidate_words.get_candidates()
            if not words:
                await cls.finish(update, context, 'Não há palavras candidatas para adicionar ao vocabulário!')
                return

            cls.words_to_process = words.copy()
            english_word = words[cls.current_index]['word']

            await cls.ask_confirm(update, context, f'Deseja add <strong>"{english_word}"</strong> ao vocabulario?', AddVocab.check_word)
        except Exception as error:
            await cls.send_error(update, context, error, sys.exc_info())

    @classmethod
    async def check_word(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, confirm_response: str):
        try:
            if confirm_response == 'no':
                english_word = cls.words_to_process[cls.current_index]['word']
                cls.candidate_words.remove_word(english_word)

                cls.current_index += 1
                if cls.current_index >= len(cls.words_to_process):
                    await cls.finish(update, context, 'Não há mais palavras candidatas para adicionar ao vocabulário!')
                    return

                english_word = cls.words_to_process[cls.current_index]['word']
                await cls.ask_confirm(update, context, f'Deseja adicionar <strong>"{english_word}"</strong> ao vocabulario?', AddVocab.check_word)
                return

            english_word = cls.words_to_process[cls.current_index]['word']

            infos_api = get_meaning_data_api(english_word)
            hint_word = infos_api.get('meaning', 'Sem definição')

            examples = infos_api.get('examples', [])
            examples.extend(cls.candidate_words.get_candidates_sentences(english_word))

            llm_infos = get_complement_data_llm(english_word, hint_word, examples)
            portuguese_word = llm_infos.get('portuguese_translation', 'Sem tradução')

            message = f"Palavra: '<strong>{english_word}</strong>'\n"
            message += f"Significado: '<strong>{portuguese_word}</strong>'\n"
            message += f"Definição: '<strong>{hint_word}</strong>'\n\n"
            message += "Exemplos:\n"

            for index, example in enumerate(examples):
                message += f"<strong>{str(index + 1)}.</strong> {example}\n"

            cls.storage_info(context, 'english_word', english_word)
            cls.storage_info(context, 'portuguese_word', portuguese_word)
            cls.storage_info(context, 'hint_word', hint_word)
            await cls.send_message(update, context, message)

            await cls.ask_confirm(update, context, 'Deseja corrigir manualmente alguma informação?', AddVocab.confirm_word)
        except Exception as error:
            await cls.send_error(update, context, error, sys.exc_info())

    @classmethod
    async def confirm_word(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, portuguese_word: str):
        try:
            portuguese_word = str(portuguese_word).upper()
            if not portuguese_word:
                await cls.finish(update, context, 'Digite o significado da palavra/expressão corretamente!')
                return

            cls.storage_info(context, 'portuguese_word', portuguese_word)
            await cls.question_message(update, context, 'Digite a definição da palavra/expressão', AddVocab.get_hint)
        except Exception as error:
            await cls.send_error(update, context, error, sys.exc_info())

    @classmethod
    async def get_hint(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, hint_word: str):
        try:
            hint_word = str(hint_word).upper()
            if not hint_word:
                await cls.finish(update, context, 'Digite o hint da palavra/expressão corretamente!')
                return

            cls.storage_info(context, 'hint_word', hint_word)
            await cls.question_message(update, context, 'Digite uma frase de exemplo', AddVocab.get_examples)
        except Exception as error:
            await cls.send_error(update, context, error, sys.exc_info())

    @classmethod
    async def get_examples(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, sentence_example: str):
        try:
            sentence_example = str(sentence_example).upper()
            if sentence_example == 'FIM':
                english_word = cls.get_info_storage(context, 'english_word')
                portuguese_word = cls.get_info_storage(context, 'portuguese_word')
                sentence_examples = cls.get_info_storage(context, 'sentence_examples')
                if not sentence_examples:
                    await cls.question_message(update, context, 'Digite uma frase de exemplo', AddVocab.get_examples)
                else:
                    message = f"Inglês: '<strong>{english_word}</strong>'\n"
                    message += f"Português: '<strong>{portuguese_word}</strong>'\n\n"
                    message += "Confirma o cadastro da palavra?"

                    await cls.ask_confirm(update, context, message, AddVocab.save_word)
            else:
                cls.append_in_storage(context, 'sentence_examples', sentence_example)
                await cls.question_message(update, context, "Digite uma frase de exemplo ou digite 'fim' para salvar os dados!", AddVocab.get_examples)
        except Exception as error:
            await cls.send_error(update, context, error, sys.exc_info())

    @classmethod
    async def save_word(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, confirm_response: str):
        try:
            if confirm_response == 'no':
                await cls.finish(update, context, 'Processo encerrado!')
                return

            english_word = cls.get_info_storage(context, 'english_word')
            portuguese_word = cls.get_info_storage(context, 'portuguese_word')
            hint_word = cls.get_info_storage(context, 'hint_word')
            sentence_examples = cls.get_info_storage(context, 'sentence_examples')

            vocabulary_model = Vocabulary()
            vocabulary_model.connect()

            training_model = TrainingState()
            training_model.connect()

            id_word = vocabulary_model.insert_line(english_word, portuguese_word, hint_word)
            training_model.insert_line(id_word)
            for sentence in sentence_examples:
                sentence_model = ExampleSentence()
                sentence_model.connect()
                sentence_model.insert_line(sentence, id_word)

            await cls.finish(update, context, 'Dados salvos com sucesso!')
        except Exception as error:
            await cls.send_error(update, context, error, sys.exc_info())
