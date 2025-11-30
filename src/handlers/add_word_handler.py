from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from src.handlers.base_handler import BaseHandler

class AddWord(BaseHandler):

    @classmethod
    async def init(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            english_word = cls.get_message(update).upper()
            if not english_word:
                await cls.finish(update, context, 'Digite uma palavra!')
                return

            cls.storage_info(context, 'english_word', english_word)
            await cls.send_message(update, context, f"Adicionando '<strong>{english_word}</strong>' ao vocabulário.")

            await cls.question_message(update, context, 'Qual o significado em português dessa palavra/expressão?', AddWord.confirm_word)
        except Exception as error:
            await cls.send_message(update, context, f'falha no AddWord:init - {error}')

    @classmethod
    async def confirm_word(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, portuguese_word: str):
        try:
            portuguese_word = str(portuguese_word).upper()
            if not portuguese_word:
                await cls.finish(update, context, 'Digite o significado da palavra/expressão corretamente!')
                return

            cls.storage_info(context, 'portuguese_word', portuguese_word)
            await cls.question_message(update, context, 'Digite uma frase de exemplo', AddWord.get_examples)
        except Exception as error:
            await cls.send_message(update, context, f'falha no AddWord:confirm_word - {error}')

    @classmethod
    async def get_examples(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, sentence_example: str):
        try:
            sentence_example = str(sentence_example).upper()
            if sentence_example == 'FIM':
                english_word = cls.get_info_storage(context, 'english_word')
                portuguese_word = cls.get_info_storage(context, 'portuguese_word')
                sentence_examples = cls.get_info_storage(context, 'sentence_examples')
                if not sentence_examples:
                    await cls.question_message(update, context, 'Digite uma frase de exemplo', AddWord.get_examples)
                else:
                    message = f"Inglês: '<strong>{english_word}</strong>'\n"
                    message += f"Português: '<strong>{portuguese_word}</strong>'\n\n"
                    message += "Confirma o cadastro da palavra?"

                    await cls.ask_confirm(update, context, message, AddWord.save_word)
            else:
                cls.append_in_storage(context, 'sentence_examples', sentence_example)
                await cls.question_message(update, context, "Digite uma frase de exemplo ou digite 'fim' para salvar os dados!", AddWord.get_examples)
        except Exception as error:
            await cls.send_message(update, context, f'falha no AddWord:confirm_word - {error}')

    @classmethod
    async def save_word(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, confirm_response: str):
        try:
            if confirm_response == 'no':
                await cls.finish(update, context, 'Processo encerrado!')
                return

            english_word = cls.get_info_storage(context, 'english_word')
            portuguese_word = cls.get_info_storage(context, 'portuguese_word')
            sentence_examples = cls.get_info_storage(context, 'sentence_examples')

            print(english_word)
            print(portuguese_word)
            for sentence in sentence_examples:
                print(sentence)

            await cls.finish(update, context, 'Dados salvos com sucesso!')
        except Exception as error:
            await cls.send_message(update, context, f'falha no AddWord:save_word - {error}')
