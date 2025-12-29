from src.database.postgres import Postgres


class IrregularVerbs(Postgres):
    def __init__(self):
        super().__init__('irregular_verbs')

    def insert_line(self, regular_form, past_simple, past_participle):
        cursor = self.connection.cursor()

        base_sql = f'INSERT INTO {self.schema}.{self.table_name}(regular_form, past_simple, past_participle) VALUES (%s, %s, %s) RETURNING id'
        cursor.execute(base_sql, (regular_form, past_simple, past_participle))

        new_id = cursor.fetchone()[0]
        self.connection.commit()
        cursor.close()

        return new_id

    def get_all_verbs(self):
        query = f"""
            select *
            from {self.schema}.{self.table_name}
            order by regular_form
        """
        result = self.select_query_dict(query, 'regular_form')
        return result
