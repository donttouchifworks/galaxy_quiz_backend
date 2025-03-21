from . import logger
from .db_model import get_db_connection, check_table_exists, create_table


def insert_question(question_data):
    """add question"""
    insert_query = """
    INSERT INTO questions (question, correct_answer, answer_1, answer_2, answer_3, answer_4, topic)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(insert_query, (
            question_data['question'],
            question_data['correct_answer'],
            question_data['options'][0],
            question_data['options'][1],
            question_data['options'][2],
            question_data['options'][3],
            question_data['topic']
        ))
        conn.commit()
        cur.close()
        conn.close()
        logger.info("question successfuly added")
    except Exception as e:
        logger.warn(f"Error during adding: {e}")


def insert_questions(questions, title):
    if not check_table_exists("questions"):
        print("Table doesn't exist. Creating...")
        create_table()
    else:
        print("Table 'questions' already exist.")
    for item in questions:
        item['topic'] = title
        insert_question(item)


def get_all_questions_db():
    select_query = "SELECT question FROM questions;"
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(select_query)
        questions = cur.fetchall()
        cur.close()
        conn.close()

        # for question in questions:
        #     logger.info(f"Question: {question[0]}")
        return questions
    except Exception as e:
        logger.warning(f"Error during retrieving questions: {e}")
        return []


def get_unasked_questions_db(asked_question_ids):
    """Retrieve questions that have not been asked to the user yet."""
    if not asked_question_ids:
        select_query = "SELECT * FROM questions;"  # return all
    else:
        placeholders = ', '.join(['%s'] * len(asked_question_ids))
        select_query = f"SELECT * FROM questions WHERE id NOT IN ({placeholders});"

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if asked_question_ids:
            cur.execute(select_query, tuple(asked_question_ids))
        else:
            cur.execute(select_query)

        unasked_questions = cur.fetchall()
        cur.close()
        conn.close()
        questions = transform_questions(unasked_questions)
        return questions
    except Exception as e:
        logger.warning(f"Error during retrieving unasked questions: {e}")
        return []


def transform_questions(data):
    transformed = []
    for item in data:
        transformed.append({
            "id": item[0],
            "question": item[1],           # Question
            "correct_answer": item[2],     # Correct answer
            "options": item[3:7],          # options
            "topic": item[7]               # topic
        })
    return transformed


def get_question_by_id_db(question_id):
    """Retrieve question by ID"""
    select_query = """
    SELECT id, question, correct_answer, answer_1, answer_2, answer_3, answer_4, topic
    FROM questions
    WHERE id = %s;
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(select_query, (question_id,))
        result = cur.fetchone()  # Retrieve a single record
        cur.close()
        conn.close()

        if result:
            question = {
                'id': result[0],
                'question': result[1],
                'correct_answer': result[2],
                'options': [result[3], result[4], result[5], result[6]],
                'topic': result[7]
            }
            return question
        else:
            logger.warn(f"No question found with ID: {question_id}")
            return None
    except Exception as e:
        logger.error(f"Error during fetching question: {e}")
        return None
