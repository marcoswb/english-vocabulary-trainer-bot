from src.database.postgres import Postgres


class CandidateWords(Postgres):
    def __init__(self):
        super().__init__('candidate_words')

    def remove_word(self, word):
        cursor = self.connection.cursor()

        base_sql = f'UPDATE {self.schema}.{self.table_name} SET active = false WHERE word = %s'
        cursor.execute(base_sql, (word,))
        self.connection.commit()

    def get_candidates(self):
        query = f"""
            select *
            from english_trainer.candidate_words
            where active = true
            order by score desc
        """

        result = self.select_query(query)
        return result
