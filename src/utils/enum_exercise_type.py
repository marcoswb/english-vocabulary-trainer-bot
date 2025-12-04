from enum import Enum

class ExerciseType(Enum):
    EN_TRANSLATION = 1  # tradução de inglês para português
    PT_TRANSLATION = 2  # tradução de português para inglês
    CLOZE_WITH_HINT_AND_SIZE = 3  # completar frase(com hint e tamanho da palavra como dica)
    CLOZE_WITH_HINT = 4  # completar frase(somente com hint como dica)
    CLOZE_WITHOUT_HINT = 5  # completar frase(sem dica)
    LEARNEAD = 6  # palavra aprendida
