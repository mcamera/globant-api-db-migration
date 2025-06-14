from fastapi import FastAPI, UploadFile


app = FastAPI()

@app.post("/departments")
async def departments(csv_file: UploadFile) -> dict:
    try:
        if not csv_file:
            return {"message": "No file sent!"}

        if not csv_file.filename.endswith('.csv'):
            return {"error": "File must be a CSV!"}
        
        contents = csv_file.file.read()
        contents = contents.decode("utf-8").splitlines()
        
        if len(contents) > 1000:
            return {"error": "File name is too long, must be less than 1000 records!"}
        elif len(contents) == 0:
            return {"error": "File is empty! Send at least 1 record."}
        else:
            return {"message": contents} 

    except Exception as e:
        return {"error": str(e)}
    

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
