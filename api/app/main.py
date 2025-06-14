from typing import Optional

from db import get_mysql_connection
from fastapi import FastAPI, File, HTTPException, UploadFile, status
from mysql.connector import ProgrammingError, errorcode
from utils import get_logger

logger = get_logger(__name__)
app = FastAPI()


@app.post("/departments")
async def departments(csv_file: Optional[UploadFile] = File(None)) -> dict:

    if not csv_file:
        logger.error("No file sent!")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No file sent!"
        )

    if not csv_file.filename.endswith(".csv"):
        logger.error("File must be a CSV!")
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="File must be a CSV!",
        )

    contents = csv_file.file.read()
    contents = contents.decode("utf-8").splitlines()

    if len(contents) > 1000:
        logger.error("Too many records! Must be less than 1000 lines.")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Too many records! Must be less than 1000 lines.",
        )
    elif len(contents) == 0:
        logger.error("File is empty! Send at least 1 record.")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File is empty! Send at least 1 record.",
        )

    # connecting to MySQL database
    db_conn = get_mysql_connection()
    cursor = db_conn.cursor()

    try:
        cursor.execute("SELECT * FROM departments;")
        results = cursor.fetchall()
        cursor.close()
        db_conn.close()

        if not results:
            logger.warning("No departments found in the table.")
            return {"message": "No departments found."}

        return [{"id": r[0], "department": r[1]} for r in results]

    except ProgrammingError as err:
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

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/jobs")
async def jobs() -> dict:
    return {"message": "jobs endpoint for send jobs data."}


@app.post("/employees")
async def employees() -> dict:
    return {"message": "Employees endpoint for send employees data."}


@app.get("/quantity_employees_hired_by_quarters/{year}")
async def quantity_employees_hired_by_quarters(year: int) -> dict:
    return {
        "message": f"Shows the quantity of employees hired by quarters from the year {year}"
    }


@app.get("/quantity_employees_hired_more_than_year_mean_by_department/{year}")
async def quantity_employees_hired_more_than_year_mean_by_department(year: int) -> dict:
    return {
        "message": f"Shows the quantity of employees hired more than year mean, by department, from the year {year}"
    }
