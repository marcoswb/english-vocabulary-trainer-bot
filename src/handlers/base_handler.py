from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


class BaseHandler:

    @classmethod
    def get_message(cls, update: Update):
        return ' '.join(update.message.text.split(' ')[1:]).strip()

    @classmethod
    async def send_message(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML")

    @classmethod
    async def send_error(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, error, exec_info):
        exc_type, exc_value, exc_tb = exec_info

        filename = exc_tb.tb_frame.f_code.co_filename
        filename = str(filename).split('english-vocabulary-trainer-bot')[1]
        line_number = exc_tb.tb_lineno
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Arquivo: {filename}: {line_number} - "{error}"', parse_mode="HTML")

    @classmethod
    async def question_message(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str, callback_func):
        context.user_data['callback_function'] = callback_func
        await cls.reply(update, message, parse_mode="HTML")

    @classmethod
    def storage_info(cls, context: ContextTypes.DEFAULT_TYPE, key: str, value):
        context.user_data[key] = value

    @classmethod
    def append_in_storage(cls, context: ContextTypes.DEFAULT_TYPE, key: str, value):
        if not context.user_data.get(key):
            context.user_data[key] = []

        context.user_data[key].append(value)

    @classmethod
    def get_info_storage(cls, context: ContextTypes.DEFAULT_TYPE, key: str):
        return context.user_data.get(key)

    @classmethod
    async def ask_confirm(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str, callback_func):
        context.user_data['callback_function'] = callback_func
        keyboard = [
            [InlineKeyboardButton('Sim', callback_data='yes')],
            [InlineKeyboardButton('Não', callback_data='no')],
        ]
        await cls.reply(
            update,
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )

    @classmethod
    async def ask_with_options(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str, options: list, callback_func, voice_mp3=None):
        context.user_data['callback_function'] = callback_func
        keyboard = []
        options.sort()
        for option in options:
            keyboard.append([InlineKeyboardButton(option, callback_data=option)])
        await cls.reply(
            update,
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )

        if voice_mp3:
            await context.bot.send_voice(chat_id=update.effective_chat.id, voice=open(voice_mp3, 'rb'))

    @classmethod
    async def mark_response(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, is_correct: bool, correct_response: str):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=(
                f'<b>Resposta correta!</b> 🎉'
                if is_correct else
                f'<b>Resposta errada.</b> ❌\n'
                f'Correto: <b>{correct_response}</b>'
            ),
           parse_mode="HTML")

    @classmethod
    async def finish(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        context.user_data.clear()
        await cls.send_message(update, context, message)

    @classmethod
    async def reply(cls, update: Update, text: str, **kwargs):
        if update.message:
            await update.message.reply_text(text, **kwargs)
        elif update.callback_query:
            await update.callback_query.message.reply_text(text, **kwargs)
