import os

import mysql.connector
from fastapi import HTTPException, status
from mysql.connector import ProgrammingError, errorcode
from utils import get_logger

logger = get_logger(__name__)


def get_mysql_connection():
    """Creates a connection to the MySQL database."""
    try:
        logger.info("Connecting to MySQL database...")
        db_conn = mysql.connector.connect(
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            host=os.getenv("MYSQL_HOST", "mysql"),
            database="database",
        )

        logger.info("MySQL database connected successfully.")

        return db_conn

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger.error("Username or password incorrect!")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username or password incorrect!",
            )

        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Username or password incorrect!",
            )
        else:
            logger.error(err)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
            )


def handle_db_errors(err: ProgrammingError):
    """Handle database errors and raise appropriate HTTP exceptions.

    Args:
        err (ProgrammingError): The error raised by the database.

    Raises:
        HTTPException: Raises an HTTPException with a status code and detail message based on the error.
    """
    if err.errno == errorcode.ER_BAD_TABLE_ERROR:
        logger.error("Table does not exist!")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Table does not exist!",
        )
    else:
        logger.error(f"MySQL Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
