from src.database.postgres import Postgres


class ExampleSentence(Postgres):
    def __init__(self):
        super().__init__('example_sentences')

    def insert_line(self, sentence, vocab_id):
        cursor = self.connection.cursor()

        base_sql = f'INSERT INTO {self.schema}.{self.table_name}(sentence, vocab_id) VALUES (%s, %s) RETURNING id'
        cursor.execute(base_sql, (sentence, vocab_id))

        new_id = cursor.fetchone()[0]
        self.connection.commit()

        return new_id
