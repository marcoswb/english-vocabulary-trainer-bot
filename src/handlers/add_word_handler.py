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

            await cls.question_message(update, context, 'Qual o significado em português dessa palavra/frase?', AddWord.confirm_word)
        except Exception as error:
            await cls.send_message(update, context, f'falha no AddWord:init - {error}')

    @classmethod
    async def confirm_word(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, portuguese_word: str):
        try:
            portuguese_word = str(portuguese_word).upper()
            if not portuguese_word:
                await cls.finish(update, context, 'Digite o significado da palavra/frase corretamente!')
                return

            cls.storage_info(context, 'portuguese_word', portuguese_word)
            english_word = cls.get_info_storage(context, 'english_word')

            message = f"Inglês: '<strong>{english_word}</strong>'\n"
            message += f"Português: '<strong>{portuguese_word}</strong>'\n\n"
            message += "Confirma o cadastro da palavra?"

            await cls.ask_confirm(update, context, message, AddWord.save_word)
        except Exception as error:
            await cls.send_message(update, context, f'falha no AddWord:confirm_word - {error}')

    @classmethod
    async def save_word(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, confirm_response: str):
        try:
            if confirm_response == 'no':
                await cls.finish(update, context, 'Processo encerrado!')
                return

            await cls.finish(update, context, 'Dados salvos com sucesso!')
        except Exception as error:
            await cls.send_message(update, context, f'falha no AddWord:save_word - {error}')
