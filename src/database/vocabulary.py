from src.database.postgres import Postgres


class Vocabulary(Postgres):
    def __init__(self):
        super().__init__('vocabulary')

    def insert_line(self, word, meaning, hint):
        cursor = self.connection.cursor()

        base_sql = f'INSERT INTO {self.schema}.{self.table_name}(word, meaning, hint) VALUES (%s, %s, %s) RETURNING id'
        cursor.execute(base_sql, (word, meaning, hint))

        new_id = cursor.fetchone()[0]
        self.connection.commit()
        cursor.close()

        return new_id
