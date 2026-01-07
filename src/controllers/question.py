import src.utils.shared as shared

class Question:

    def __init__(self, vocab_id=None, question=None, correct_response=None, hint=None, options=None, first_word=False, english_word=None, send_mp3_with_question=False):
        self.__vocab_id = vocab_id
        self.__question: str = question
        self.__correct_response = str(correct_response).upper()
        self.__hint: str = hint
        self.__first_word: bool = first_word
        self.__send_mp3_with_question: bool = send_mp3_with_question
        self.__english_word: str = english_word
        self.__options: list = None
        if options:
            self.__options = [str(item).upper() for item in options]
        else:
            self.remove_word_sentence()

    def get_question(self):
        return self.__question

    def get_english_word(self):
        return self.__english_word

    def send_mp3_with_question(self):
        return self.__send_mp3_with_question

    def get_response(self):
        return self.__correct_response

    def get_options(self):
        return self.__options

    def get_hint(self):
        return self.__hint

    def get_vocab_id(self):
        return self.__vocab_id

    def remove_word_sentence(self):
        if self.__correct_response not in self.__question:
            self.__correct_response = str(self.__correct_response).split(' ')[0]

        if self.__correct_response not in self.__question and self.__correct_response in shared.dic_irregular_verbs:
            aux_verb = shared.dic_irregular_verbs.get(self.__correct_response)
            if aux_verb.get('past_simple') in self.__question:
                self.__correct_response = aux_verb.get('past_simple')
            elif aux_verb.get('past_participle') in self.__question:
                self.__correct_response = aux_verb.get('past_participle')

        if self.__correct_response in self.__question:
            aux_pos = self.__question.find(self.__correct_response)
            word_response = str(self.__correct_response)
            next_character = self.__question[aux_pos+len(word_response)]

            while next_character.isalpha():
                word_response += next_character
                next_character = self.__question[aux_pos+len(word_response)]

            self.__correct_response = str(word_response)
            if self.__first_word:
                self.__question = str(self.__question).replace(self.__correct_response, self.__correct_response[0] + '_' * (len(self.__correct_response) -1))
            else:
                self.__question = str(self.__question).replace(self.__correct_response, '_' * (len(self.__correct_response)))


    def __str__(self):
        print_obj = {
            'question': self.__question,
            'correct_response': self.__correct_response,
            'options': self.__options,
            'hint': self.__hint
        }
        return str(print_obj)
