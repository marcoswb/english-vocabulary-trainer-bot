import os
from dotenv import load_dotenv

def get_env(environment):
    if not os.getenv(environment):
        load_dotenv()

    return os.getenv(environment)