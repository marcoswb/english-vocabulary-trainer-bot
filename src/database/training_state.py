from datetime import datetime

from src.database.postgres import Postgres


class TrainingState(Postgres):
    def __init__(self):
        super().__init__('training_state')

    def insert_line(self, vocab_id):
        current_date = datetime.now().date()
        next_day = current_date.replace(day=(current_date.day + 1))
        cursor = self.connection.cursor()

        base_sql = f'INSERT INTO {self.schema}.{self.table_name}(vocab_id, streak, confidence, last_review, next_review) VALUES (%s, %s, %s, %s, %s) RETURNING id'
        cursor.execute(base_sql, (vocab_id, 0, 0, current_date, next_day))

        new_id = cursor.fetchone()[0]
        self.connection.commit()
        cursor.close()

        return new_id
