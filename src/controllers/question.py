class Question:

    def __init__(self, vocab_id=None, question=None, correct_response=None, hint=None, options=None):
        self.__vocab_id = vocab_id
        self.__question = question
        self.__correct_response = correct_response
        self.__hint = hint
        self.__options = options

    def get_question(self):
        return self.__question

    def get_response(self):
        return self.__correct_response

    def get_options(self):
        return self.__options

    def get_hint(self):
        return self.__hint

    def get_vocab_id(self):
        return self.__vocab_id

    def __str__(self):
        print_obj = {
            'question': self.__question,
            'correct_response': self.__correct_response,
            'options': self.__options,
            'hint': self.__hint
        }
        return str(print_obj)
