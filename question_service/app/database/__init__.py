from .db_model import get_db_connection,check_table_exists,create_table
from time import sleep
from .. import app, logger


def init_db():
    print("connecting to db...")
    while True:
        try:
            conn = get_db_connection()
            logger.info("connection to questions db installed.")
            conn.close()
            logger.info("checking if table exist ...")
            if check_table_exists("questions"):
                break
            else:
                logger.info("Table doesn't exist, creating table...")
                create_table()
                continue
            # while check_table_exists("questions"):
            #     try:
            #         create_table()
            #         break
            #     except Exception as e:
            #         logger.info(f"failed to create table, error: {e}")
            #         sleep(2)
            break
        except:
            print("connecting to db failed restarting...")
            sleep(2)