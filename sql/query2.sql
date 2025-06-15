-- List of ids, name and number of employees hired of each department that hired more
-- employees than the mean of employees hired in 2021 for all the departments, ordered
-- by the number of employees hired (descending).
WITH CTE_TOTAL_HIRED_BY_DEP AS (
    SELECT
        department_id,
        COUNT(1) AS hired
    FROM employees
    WHERE YEAR(datetime) = 2021
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
