from typing import Optional

from db import insert_into_table
from fastapi import FastAPI, File, UploadFile
from utils import get_logger
from validations import validate_csv_file, validate_upload_file

logger = get_logger(__name__)
app = FastAPI()


@app.post("/departments")
async def departments(csv_file: Optional[UploadFile] = File(None)) -> dict:
    validate_upload_file(csv_file)

    contents = csv_file.file.read()
    csv_rows = contents.decode("utf-8").strip().splitlines()
    validate_csv_file(csv_rows, max_lines=1000)

    csv_file.file.seek(0)
    result = insert_into_table(
        csv_rows, table_name="departments", columns="id, department"
    )

    csv_file.file.close()

    return result


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
