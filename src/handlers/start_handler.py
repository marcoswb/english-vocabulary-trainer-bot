from telegram import Update
from telegram.ext import ContextTypes
from src.handlers.base_handler import BaseHandler
from src.database.training_state import TrainingState


class Start(BaseHandler):

    @classmethod
    async def init(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        training_model = TrainingState()
        training_model.connect()

        training_words = training_model.get_vocabs_to_training()
        print(training_words)
