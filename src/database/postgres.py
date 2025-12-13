import psycopg2
from src.utils.functions import get_env


class Postgres:
    opened_connection = None

    def __init__(self, table_name):
        self.connection = None
        self.schema = 'english_trainer'
        self.table_name = str(table_name)

    @classmethod
    def get_connection(cls):
        return cls.opened_connection

    def connect(self):
        if not Postgres.get_connection():
            Postgres.opened_connection = psycopg2.connect(
                                    dbname=get_env('DB_DATABASE'),
                                    user=get_env('DB_USER'),
                                    password=get_env('DB_PASSWORD'),
                                    host=get_env('DB_HOST'),
                                    port=5432
                                )

        self.connection = Postgres.get_connection()

    def select_all(self):
        cursor = self.connection.cursor()

        cursor.execute(f'SELECT * FROM {self.schema}.{self.table_name}')
        result_db = cursor.fetchall()
        header = [desc[0] for desc in cursor.description]

        list_result = []
        for line in result_db:
            list_result.append(dict(zip(header[1:], line[1:])))

        cursor.close()
        return list_result

    def select_query(self, query: str, args=()):
        cursor = self.connection.cursor()
        cursor.execute(query, args)
        result_db =  cursor.fetchall()
        header = [desc[0] for desc in cursor.description]

        list_result = []
        for line in result_db:
            list_result.append(dict(zip(header, line)))
        return list_result

    def select_without_header(self, query: str, args=()):
        cursor = self.connection.cursor()
        cursor.execute(query, args)
        result_db =  cursor.fetchall()

        list_result = []
        for line in result_db:
            list_result.append(line[0])
        return list_result

    def select_query_dict(self, query: str, key_dict: str, args=()):
        cursor = self.connection.cursor()
        cursor.execute(query, args)
        result_db =  cursor.fetchall()
        header = [desc[0].lower() for desc in cursor.description]

        dict_result = {}
        for line in result_db:
            dict_line = dict(zip(header, line))
            dict_result[dict_line.get(key_dict.lower())] = dict_line
        return dict_result

    def clear_table(self):
        cursor = self.connection.cursor()

        sql_script = f'DELETE FROM {self.schema}.{self.table_name}'
        cursor.execute(sql_script)

        cursor.close()
        self.connection.commit()