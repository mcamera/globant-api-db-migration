from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile, status

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


@app.post("/jobs")
async def jobs() -> dict:
    return {"message": "jobs endpoint for send jobs data."}

@app.post("/employees")
async def employees() -> dict:
    return {"message": "Employees endpoint for send employees data."}

@app.get("/quantity_employees_hired_by_quarters/{year}")
async def quantity_employees_hired_by_quarters(year: int) -> dict:
    return {"message": f"Shows the quantity of employees hired by quarters from the year {year}"}

@app.get("/quantity_employees_hired_more_than_year_mean_by_department/{year}")
async def quantity_employees_hired_more_than_year_mean_by_department(year: int) -> dict:
    return {"message": f"Shows the quantity of employees hired more than year mean, by department, from the year {year}"}
