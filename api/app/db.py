import os

import mysql.connector
from mysql.connector import errorcode

from utils import get_logger

logger = get_logger(__name__)


def get_mysql_connection():

    try:
        logger.info("Connecting to MySQL database...")
        db_conn = mysql.connector.connect(
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            host="mysql",
            database="database",
        )

        logger.info("MySQL database connected successfully.")
        return db_conn

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger.error("User name or password incorrect!")
            return err
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger.error("Database does not exist!")
            return {**err, "message": "Database does not exist!"}
        else:
            logger.error(err)
            return err
