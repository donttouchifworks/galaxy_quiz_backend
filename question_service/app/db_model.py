import psycopg2
from flask import current_app
from app import logger, app


def get_db_connection():
    return psycopg2.connect(
        host=app.config["DB_HOST"],
        database=app.config["DB_NAME"],
        user=app.config["DB_USER"],
        password=app.config["DB_PASSWORD"],
        port=app.config["DB_PORT"]
    )


def check_table_exists():
    check_query = """
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_name = 'questions'
    );
    """

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(check_query)
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        return result
    except Exception as e:
        logger.warn(f"Table doesn't exist: {e}")
        return False


def create_table():
    """create table"""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS questions (
        id SERIAL PRIMARY KEY,
        question TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        answer_1 TEXT NOT NULL,
        answer_2 TEXT NOT NULL,
        answer_3 TEXT NOT NULL,
        answer_4 TEXT NOT NULL,
        topic TEXT NOT NULL
    );
    """

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        logger.info(f"status: success, 'db_version': {db_version}")
    except Exception as e:
        logger.warn(f"Connecting to DB at {app.config['DB_HOST']}:{app.config['DB_PORT']}")
        logger.warn(f"'status': 'error', 'error': {str(e)}")
