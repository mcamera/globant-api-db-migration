-- This SQL script will create all the necessary tables when the database is initialized for the first time.
CREATE TABLE IF NOT EXISTS departments (
    id INT PRIMARY KEY,
    department VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS jobs (
    id INT PRIMARY KEY,
    job VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS employees (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    datetime DATETIME NOT NULL,
    department_id INT NOT NULL,
    job_id INT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);
