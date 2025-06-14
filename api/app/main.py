from typing import Optional

from db import get_mysql_connection, handle_db_errors
from fastapi import FastAPI, File, HTTPException, UploadFile, status
from mysql.connector import ProgrammingError
from utils import get_logger, validate_upload_file

logger = get_logger(__name__)
app = FastAPI()


@app.post("/departments")
async def departments(csv_file: Optional[UploadFile] = File(None)) -> dict:
    validate_upload_file(csv_file, max_lines=1000)

    db_conn = get_mysql_connection()
    cursor = db_conn.cursor()

    try:
        cursor.execute("SELECT * FROM departments;")
        results = cursor.fetchall()

        if not results:
            logger.warning("No departments found in the table.")
            return {"message": "No departments found."}

    except ProgrammingError as err:
        handle_db_errors(err)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    finally:
        cursor.close()
        db_conn.close()


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
