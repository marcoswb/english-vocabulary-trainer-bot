from src.database.postgres import Postgres


class CandidateWords(Postgres):
    def __init__(self):
        super().__init__('candidate_words')
        self.__table_sentences = 'candidate_words_sentences'

    def remove_word(self, word):
        cursor = self.connection.cursor()

        base_sql = f'UPDATE {self.schema}.{self.table_name} SET active = false WHERE word = %s'
        cursor.execute(base_sql, (word,))
        self.connection.commit()

    def get_candidates(self):
        query = f"""
            select *
            from {self.schema}.{self.table_name}
            where active = true
            order by score desc
        """

        result = self.select_query(query)
        return result

    def get_candidates_sentences(self, word):
        query = f"""
            select sentence
            from {self.schema}.{self.__table_sentences}
            where id_word = (select max(id) from {self.schema}.{self.table_name} where word = '{word}')
        """

        result = self.select_without_header(query)
        return result
