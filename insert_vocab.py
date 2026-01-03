import psycopg2
from src.utils.functions import get_env

DB_CONFIG = {
    'host': get_env('DB_HOST'),
    'dbname': get_env('DB_DATABASE'),
    'user': get_env('DB_USER'),
    'password': get_env('DB_PASSWORD'),
    'port': 5432
}

BASE_PATH = 'data'


def load_vocabulary(cursor):
    with open(f'{BASE_PATH}/vocabulary.txt', encoding='utf-8') as f:
        for line in f:
            word, meaning, hint = line.strip().split('\t')

            cursor.execute(
                """
                INSERT INTO english_trainer.vocabulary (word, meaning, hint)
                VALUES (%s, %s, %s)
                """,
                (word, meaning, hint)
            )


def load_training_state(cursor):
    with open(f'{BASE_PATH}/vocabulary.txt', encoding='utf-8') as f:
        for line in f:
            word, _, _ = line.strip().split('\t')

            cursor.execute(
                """
                INSERT INTO english_trainer.training_state
                (vocab_id, streak, last_review, next_review, confidence)
                SELECT id, 0, CURRENT_DATE, CURRENT_DATE, 0
                FROM english_trainer.vocabulary
                WHERE word = %s
                """,
                (word, )
            )


def load_example_sentences(cursor):
    with open(f'{BASE_PATH}/example_sentences.txt', encoding='utf-8') as f:
        for line in f:
            word, sentence = line.strip().split('\t')

            cursor.execute(
                """
                INSERT INTO english_trainer.example_sentences (vocab_id, sentence)
                SELECT id, %s
                FROM english_trainer.vocabulary
                WHERE word = %s
                """,
                (sentence, word)
            )


def save_table(name_table, cursor):
    with open(f'./resource/data_{name_table}.txt', 'w', encoding='utf-8') as f:
        cursor.execute(f'SELECT * FROM english_trainer.{name_table} ORDER BY 1')
        result_db = cursor.fetchall()

        f.write('\t'.join([desc[0].lower() for desc in cursor.description]))
        f.write('\n')
        for line in result_db:
            f.write('\t'.join([str(column) for column in line]))
            f.write('\n')


def main():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn:
            with conn.cursor() as cursor:
                print('Carregando dados.')

                load_vocabulary(cursor)
                load_training_state(cursor)
                load_example_sentences(cursor)

                print('Dados carregados com sucesso.')

                print('Realizando backup dos dados.')

                save_table('vocabulary', cursor)
                save_table('training_state', cursor)
                save_table('example_sentences', cursor)

                print('Backup realizado com sucesso.')

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()


if __name__ == '__main__':
    main()
