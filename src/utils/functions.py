import os
from dotenv import load_dotenv
from datetime import datetime
import random
from gtts import gTTS


def get_env(environment):
    if not os.getenv(environment):
        load_dotenv()

    return os.getenv(environment)


def get_current_date():
    return datetime.now().date()


def get_current_datetime():
    return datetime.now()


def get_random_itens(list_itens: list, number_itens, word: str=None):
    list_itens = [aux.upper() for aux in list_itens]
    if word:
        list_itens.remove(word.upper())
    return random.sample(list_itens, number_itens)

def get_audio_word(word):
    try:
        file = f'.\\data\\{word}.mp3'
        tts = gTTS(text=word, lang='en')
        tts.save(file)
        return file
    except:
        return None
