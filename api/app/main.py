from typing import Optional

from db import get_mysql_connection, handle_db_errors
from fastapi import FastAPI, File, HTTPException, UploadFile, status
from mysql.connector import Error, ProgrammingError
from utils import get_logger, validate_upload_file

logger = get_logger(__name__)
app = FastAPI()


@app.post("/departments")
async def departments(csv_file: Optional[UploadFile] = File(None)) -> dict:
    validate_upload_file(csv_file, max_lines=1000)

    csv_file.file.seek(0)
    contents = csv_file.file.read()
    decoded_data = contents.decode("utf-8")
    rows = decoded_data.strip().splitlines()
    rows_tuples = [tuple(row.split(",")) for row in rows]

    db_conn = get_mysql_connection()
    cursor = db_conn.cursor()

    try:
        total_rows = len(rows_tuples)

        cursor.executemany(
            "INSERT INTO departments (id, department) VALUES (%s, %s)", rows_tuples
        )
        db_conn.commit()

        logger.info(f"Total of {total_rows} departments data inserted successfully.")
        return {
            "message": f"Total of {total_rows} departments data inserted successfully."
        }

    except (ProgrammingError, Error) as err:
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
