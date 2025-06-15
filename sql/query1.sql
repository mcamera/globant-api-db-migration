-- Number of employees hired for each job and department in 2021 divided by quarter.
-- Ordered alphabetically by department and job
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
    WHERE YEAR(e.datetime) = 2021
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
ORDER BY department, job;
