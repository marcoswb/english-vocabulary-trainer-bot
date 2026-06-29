import os
from dotenv import load_dotenv
from datetime import datetime
import random
from gtts import gTTS
import requests
from google import genai
from pydantic import BaseModel
import json


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

def get_meaning_data_api(word):
    result_data = {'word': word, 'partOfSpeech': None, 'meaning': None, 'examples': []}
    try:
        request = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')

        if request.status_code == 200:
            data = request.json()
            if data and isinstance(data, list):
                for meaning in data[0].get('meanings', []):
                    if not result_data['meaning']:
                        result_data['meaning'] = meaning.get('definitions', [{}])[0].get('definition')
                        result_data['partOfSpeech'] = meaning.get('partOfSpeech')
                    else:
                        if meaning.get('partOfSpeech') == 'verb':
                            old_meaning = result_data['meaning']
                            if old_meaning != 'verb':
                                result_data['meaning'] = meaning.get('definitions', [{}])[0].get('definition')
                                result_data['partOfSpeech'] = meaning.get('partOfSpeech')


                    result_data['examples'] = [definition.get('example') for definition in meaning.get('definitions', []) if definition.get('example')]
    finally:
        return result_data

def get_complement_data_llm(word, meaning, examples):
    class ResponseText(BaseModel):
        portuguese_translation: str
        short_hint: str
        cefr_level: str

    result_data = {}
    try:
        text_examples = ''
        if examples:
            text_examples = '\n'.join(examples)
        input_text = f"""
        You are creating metadata for an English vocabulary learning app.
        Word:
        {word}
        
        Meaning:
        {meaning}
        
        Examples:
        {text_examples}
        
        Return JSON only with:
        
        - portuguese_translation
        - short_hint
        - cefr_level
        """

        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=input_text,
            config={
                "response_mime_type": "application/json",
                "response_schema": ResponseText,
            },
        )

        text = response.text.strip()
        result_data = json.loads(text)
    finally:
        return result_data
