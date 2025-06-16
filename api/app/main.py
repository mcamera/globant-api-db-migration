from typing import Optional

from app.db import delete_table, execute_query, insert_into_table
from app.utils import get_logger
from app.validations import validate_csv_file, validate_upload_file
from fastapi import FastAPI, File, UploadFile

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
async def jobs(csv_file: Optional[UploadFile] = File(None)) -> dict:
    validate_upload_file(csv_file)

    contents = csv_file.file.read()
    csv_rows = contents.decode("utf-8").strip().splitlines()
    validate_csv_file(csv_rows, max_lines=1000)

    csv_file.file.seek(0)
    result = insert_into_table(csv_rows, table_name="jobs", columns="id, job")

    csv_file.file.close()

    return result


@app.post("/employees")
async def employees(csv_file: Optional[UploadFile] = File(None)) -> dict:
    validate_upload_file(csv_file)

    contents = csv_file.file.read()
    csv_rows = contents.decode("utf-8").strip().splitlines()
    validate_csv_file(csv_rows, max_lines=1000)

    csv_file.file.seek(0)
    result = insert_into_table(
        csv_rows,
        table_name="employees",
        columns="id, name, datetime, department_id, job_id",
    )

    csv_file.file.close()

    return result


@app.delete("/departments")
async def delete_departments() -> dict:
    result = delete_table(table_name="departments")
    return result


@app.delete("/jobs")
async def delete_jobs() -> dict:
    result = delete_table(table_name="jobs")
    return result


@app.delete("/employees")
async def delete_employees() -> dict:
    result = delete_table(table_name="employees")
    return result


@app.get("/total_employees_hired_by_quarters/{year}")
async def total_employees_hired_by_quarters(year: int) -> dict:
    query_name = "total_employees_hired_by_quarters"
    result = execute_query(
        query="""
            WITH CTE AS (
                SELECT
                    department,
                    job,
                    YEAR(e.datetime) as year,
                    MONTH(e.datetime) as month,
                    CASE WHEN MONTH(e.datetime) IN (1,2,3) THEN 1 ELSE 0 END AS Q1,
                    CASE WHEN MONTH(e.datetime) IN (4,5,6) THEN 1 ELSE 0 END AS Q2,
                    CASE WHEN MONTH(e.datetime) IN (7,8,9) THEN 1 ELSE 0 END AS Q3,
                    CASE WHEN MONTH(e.datetime) IN (10,11,12) THEN 1 ELSE 0 END AS Q4
                FROM employees AS e
                JOIN departments AS d on e.department_id = d.id
                JOIN jobs AS j on e.job_id = j.id
                WHERE YEAR(e.datetime) = %s
            )
            SELECT
                department,
                job,
                CAST(SUM(Q1) as UNSIGNED) AS Q1,
                CAST(SUM(Q2) as UNSIGNED) AS Q2,
                CAST(SUM(Q3) as UNSIGNED) AS Q3,
                CAST(SUM(Q4) as UNSIGNED) AS Q4
            FROM CTE
            GROUP BY department, job
            ORDER BY department, job;""",
        year=year,
    )

    details = []
    total_rows = len(result)
    for (department, job, Q1, Q2, Q3, Q4) in result:
        details.append(
            {
                "department": department,
                "job": job,
                "Q1": Q1,
                "Q2": Q2,
                "Q3": Q3,
                "Q4": Q4,
            }
        )

    logger.info(f"Query {query_name} executed successfully.")
    return {"total_employees_hired": total_rows, "year": year, "details": details}


@app.get("/total_employees_hired_more_than_year_mean_by_department/{year}")
async def total_employees_hired_more_than_year_mean_by_department(year: int) -> dict:
    query_name = "total_employees_hired_more_than_year_mean_by_department"
    result = execute_query(
        query="""
            WITH CTE_TOTAL_HIRED_BY_DEP AS (
                SELECT
                    department_id,
                    COUNT(1) AS hired
                FROM employees
                WHERE YEAR(datetime) = %s
                GROUP BY department_id
            ),
            CTE_AVG_HIRED AS (
                SELECT
                    AVG(hired) AS avg_hired
                FROM CTE_TOTAL_HIRED_BY_DEP
            )

            SELECT
                id,
                department,
                hired
            FROM CTE_TOTAL_HIRED_BY_DEP AS dep
            JOIN departments AS d ON d.id = dep.department_id
            JOIN CTE_AVG_HIRED AS avg_hired
            WHERE dep.hired > avg_hired.avg_hired
            ORDER BY hired DESC;
        """,
        year=year,
    )

    details = []
    total_rows = len(result)
    for id, department, hired in result:
        details.append(
            {
                "id": id,
                "department": department,
                "hired": hired,
            }
        )

    logger.info(f"Query {query_name} executed successfully.")
    return {"total_departments_hired": total_rows, "year": year, "details": details}
