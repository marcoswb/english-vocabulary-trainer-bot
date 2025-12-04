import os
from dotenv import load_dotenv
from datetime import datetime
import random


def get_env(environment):
    if not os.getenv(environment):
        load_dotenv()

    return os.getenv(environment)


def get_current_date():
    return datetime.now().date()


def get_random_itens(list_itens, number_itens):
    return random.sample(list_itens, number_itens)
