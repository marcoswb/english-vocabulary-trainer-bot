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
        query = f"""
            select ts.vocab_id,
                   ts.streak,
                   ts.confidence,
                   vb.word,
                   vb.meaning,
                   vb.hint
            from {self.schema}.{self.table_name} ts
            inner join {self.schema}.vocabulary vb
                on ts.vocab_id = vb.id
            where ts.next_review <= %s
            order by ts.next_review, ts.streak
        """
        result = self.select_query(query, (current_date, ))
        return result

    def get_vocabs_score(self):
        current_date = get_current_date()
        query = f"""
            select ts.vocab_id,
                   ts.streak,
                   ts.confidence
            from {self.schema}.{self.table_name} ts
        """
        result = self.select_query_dict(query, 'vocab_id', (current_date, ))
        return result

    def change_confidence(self, vocabs_id: list, increase=None, decrease=None):
        if not vocabs_id:
            return

        current_date = get_current_date()
        cursor = self.connection.cursor()

        if increase:
            base_sql = f'UPDATE {self.schema}.{self.table_name} SET confidence = confidence +1, last_review = %s WHERE vocab_id IN ({", ".join(vocabs_id)})'
        elif decrease:
            base_sql = f'UPDATE {self.schema}.{self.table_name} SET confidence = confidence -1, last_review = %s WHERE vocab_id IN ({", ".join(vocabs_id)})'
        else:
            return

        cursor.execute(base_sql, (current_date, ))
        self.connection.commit()
        cursor.close()

    def change_streak(self, vocabs_id: list, increase=None, decrease=None):
        if not vocabs_id:
            return

        current_date = get_current_date()
        cursor = self.connection.cursor()

        if increase:
            base_sql = f'UPDATE {self.schema}.{self.table_name} SET streak = streak +1, last_review = %s WHERE vocab_id IN ({", ".join(vocabs_id)})'
        elif decrease:
            base_sql = f'UPDATE {self.schema}.{self.table_name} SET streak = streak -1, last_review = %s WHERE vocab_id IN ({", ".join(vocabs_id)})'
        else:
            return

        cursor.execute(base_sql, (current_date, ))
        self.connection.commit()
        cursor.close()

    def update_last_review(self, vocabs_id: list):
        if not vocabs_id:
            return

        current_date = get_current_date()
        cursor = self.connection.cursor()

        base_sql = f'UPDATE {self.schema}.{self.table_name} SET last_review = %s WHERE vocab_id IN ({", ".join(vocabs_id)})'
        cursor.execute(base_sql, (current_date, ))
        self.connection.commit()
        cursor.close()
