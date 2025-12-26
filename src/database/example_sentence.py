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

    def get_sentences_by_vocab(self, vocabs=None):
        if vocabs:
            query = f"""
                select vocab_id,
                       sentence
                from english_trainer.example_sentences
                where vocab_id in ({', '.join([str(vocab) for vocab in vocabs])})
            """
        else:
            query = f"""
                select vocab_id,
                       sentence
                from english_trainer.example_sentences
            """

        result_db = self.select_query(query, (vocabs, ))
        result = {}
        for line in result_db:
            result.setdefault(line.get('vocab_id'), [])
            result[line.get('vocab_id')].append(str(line.get('sentence')).upper())

        return result
