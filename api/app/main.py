from fastapi import FastAPI


app = FastAPI()

@app.post("/departments")
async def departments():
    return {"message": "departments endpoint for send departments data."}

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
