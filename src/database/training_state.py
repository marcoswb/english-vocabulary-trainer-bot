from src.database.postgres import Postgres
from src.utils.functions import get_current_date


class TrainingState(Postgres):
    def __init__(self):
        super().__init__('training_state')

    def insert_line(self, vocab_id):
        current_date = get_current_date()
        cursor = self.connection.cursor()

        base_sql = f'INSERT INTO {self.schema}.{self.table_name}(vocab_id, streak, confidence, last_review, next_review) VALUES (%s, %s, %s, %s, %s) RETURNING id'
        cursor.execute(base_sql, (vocab_id, 0, 0, current_date, current_date))

        new_id = cursor.fetchone()[0]
        self.connection.commit()
        cursor.close()

        return new_id

    def get_vocabs_to_training(self):
        current_date = get_current_date()
        query = """
            select vocab_id, streak, confidence
            from english_trainer.training_state
            where next_review <= %s
            order by next_review
        """
        result = self.select_query(query, (current_date, ))
        return result
