from enum import Enum

class ExerciseType(Enum):
    EN_TRANSLATION = 0  # tradução de inglês para português
    PT_TRANSLATION = 1  # tradução de português para inglês
    CLOZE_WITH_HINT_AND_FIRST_WORD = 2  # completar frase(com hint e primeira letra como dica)
    CLOZE_WITH_HINT = 3  # completar frase(somente com hint como dica)
    CLOZE_WITHOUT_HINT = 4  # completar frase(sem dica)
    LEARNEAD = 5  # palavra aprendida

    @staticmethod
    def get_exercise_by_streak(streak):
        try:
            return ExerciseType(streak)
        except:
            return None
