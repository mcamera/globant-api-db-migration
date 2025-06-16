import os
from typing import Union

import mysql.connector
from app.utils import fix_datetime, get_logger
from app.validations import check_valid_rows
from fastapi import HTTPException, status
from mysql.connector import Error, ProgrammingError, errorcode

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


def handle_db_errors(err: Union[ProgrammingError, mysql.connector.Error]) -> None:
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
    elif err.errno == errorcode.ER_DUP_ENTRY:
        logger.error("Duplicate entry found!")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Duplicate entry found!, error: {err}",
        )
    else:
        logger.error(f"MySQL Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )


def insert_into_table(csv_rows, table_name: str, columns: str):
    """Insert data into a specified MySQL table.

    Args:
        csv_file (_type_): The CSV file containing data to be inserted.
        table_name (str): The name of the table where data will be inserted.
        columns (str): A comma-separated string of column names in the table.

    Raises:
        HTTPException: If there is an error during the database operation, an HTTPException is raised with a status code and detail message.
    """
    rows_tuples = [tuple(row.split(",")) for row in csv_rows]

    db_conn = get_mysql_connection()
    cursor = db_conn.cursor()

    try:
        total_rows = len(rows_tuples)
        if table_name == "employees":
            rows_tuples_fixed = fix_datetime(rows_tuples)
            valid_rows, result = check_valid_rows(rows_tuples_fixed)
            cursor.executemany(
                f"INSERT INTO {table_name} ({columns}) VALUES (%s, %s, %s, %s, %s);",
                valid_rows,
            )
        else:  # jobs and departments tables
            cursor.executemany(
                f"INSERT INTO {table_name} ({columns}) VALUES (%s, %s);", rows_tuples
            )
        db_conn.commit()
        cursor.close()
        db_conn.close()

        if result:
            logger.info(result)
            return result
        else:
            logger.info(
                f"Total of {total_rows} {table_name} data inserted successfully."
            )
            return {
                "message": f"Total of {total_rows} {table_name} data inserted successfully."
            }

    except (ProgrammingError, Error) as err:
        handle_db_errors(err)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


def delete_table(table_name: str) -> dict:
    """Delete all data from a specified MySQL table.

    Args:
        table_name (str): The name of the table from which data will be deleted.

    Returns:
        dict: A dictionary containing a success message.
    """
    db_conn = get_mysql_connection()
    cursor = db_conn.cursor()

    try:
        cursor.execute(f"DELETE FROM {table_name};")
        db_conn.commit()
        cursor.close()
        db_conn.close()

        logger.info(f"All data from {table_name} deleted successfully.")
        return {"message": f"All data from {table_name} deleted successfully."}

    except (ProgrammingError, Error) as err:
        handle_db_errors(err)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


def execute_query(query: str, year: int) -> dict:
    """Execute a custom SQL query on the MySQL database.

    Args:
        query (str): The SQL query to be executed.
        year(int): Year to filter the result

    Returns:
        dict: A dictionary containing the result of the query execution.
    """
    db_conn = get_mysql_connection()
    cursor = db_conn.cursor()

    result = []
    try:
        cursor.execute(query, (year,))
        rows = cursor.fetchall()

        for row in rows:
            result.append(row)

        cursor.close()
        db_conn.close()

        return result

    except (ProgrammingError, Error) as err:
        handle_db_errors(err)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
