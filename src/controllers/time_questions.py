from src.utils.functions import get_current_datetime

class TimeQuestions:

    TOTAL_TIME = 30
    FIRST_LEVEL = 0.4
    SECOND_LEVEL = 0.7
    THIRD_LEVEL = 0.9
    FOURTH_LEVEL = 1

    END_FIRST_LEVEL = (TOTAL_TIME * FIRST_LEVEL)
    END_SECOND_LEVEL = (TOTAL_TIME * SECOND_LEVEL)
    END_THIRD_LEVEL = (TOTAL_TIME * THIRD_LEVEL)

    START_TIME = None
    CURRENT_LEVEL = None

    @classmethod
    def start_questions(cls):
        cls.START_TIME = get_current_datetime()
        cls.CURRENT_LEVEL = 1

    @classmethod
    def change_level(cls):
        difference_between_times = int((get_current_datetime() - cls.START_TIME) / 60)

        if difference_between_times >= cls.END_FIRST_LEVEL and cls.CURRENT_LEVEL == 1:
            cls.CURRENT_LEVEL = 2
            return True
        elif difference_between_times >= cls.END_SECOND_LEVEL and cls.CURRENT_LEVEL == 2:
            cls.CURRENT_LEVEL = 3
            return True
        elif difference_between_times >= cls.END_THIRD_LEVEL and cls.CURRENT_LEVEL == 3:
            cls.CURRENT_LEVEL = 4
            return True
        else:
            return False

    @classmethod
    def is_finished(cls):
        difference_between_times = int((get_current_datetime() - cls.START_TIME) / 60)
        return difference_between_times > cls.TOTAL_TIME
