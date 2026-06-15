import mysql
import logging


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="rental_api"
    )

logger = logging.getLogger(__name__)




if __name__=="__main__":
    logger.info("get connection")

