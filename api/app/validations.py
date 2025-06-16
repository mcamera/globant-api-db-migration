from app.utils import get_logger
from fastapi import HTTPException, UploadFile, status


def validate_upload_file(csv_file: UploadFile) -> None:
    """Validates the uploaded CSV file if it exists and is of the correct type.

    Args:
        csv_file (UploadFile): The uploaded CSV file.

    Raises:
        HTTPException: If the file is not provided, is not a CSV.
    """
    logger = get_logger(__name__)

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


def validate_csv_file(csv_rows: list[str], max_lines: int = 1000) -> None:
    """Validates the content of the CSV file if the number of lines is within the allowed limit and the file is not empty.

    Args:
        csv_rows (list[str]): List of rows from the CSV file.
        max_lines (int): Maximum number of lines allowed in the CSV file.

    Raises:
        HTTPException: If the number of lines exceeds the maximum allowed or if the file is empty.
    """
    logger = get_logger(__name__)

    if len(csv_rows) > max_lines:
        logger.error(f"Too many records! Must be less than {max_lines} lines.")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Too many records! Must be less than {max_lines} lines.",
        )

    if len(csv_rows) == 0:
        logger.error("File is empty! Send at least 1 record.")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File is empty! Send at least 1 record.",
        )


def check_valid_rows(rows_tuples: list[tuple]) -> tuple[list[tuple], dict]:
    """Check if the rows are valid.

    Args:
        rows_tuples (list[tuple]): List of tuples containing data from the CSV file.

    Returns:
        tuple: A tuple containing two elements:
            - list[tuple]: List of valid rows that can be inserted into the database.
            - dict: A dictionary containing the total number of inserted rows, rejected rows, and details of rejected records.
    """
    valid_rows = []
    result = {"total_inserted_rows": 0, "total_rejected_rows": 0, "reject_records": []}

    for index, row in enumerate(rows_tuples, start=1):
        row_errors = []
        id = row[0] if len(row) > 0 else None
        name = row[1] if len(row) > 1 else None
        dt = row[2] if len(row) > 2 else None
        department_id = row[3] if len(row) > 3 else None
        job_id = row[4] if len(row) > 4 else None

        if not id:
            row_errors.append("Missing value for 'id'")
        if not name:
            row_errors.append("Missing value for 'name'")
        if not dt:
            row_errors.append("Missing value for 'datetime'")
        if not department_id:
            row_errors.append("Missing value for 'department_id'")
        if not job_id:
            row_errors.append("Missing value for 'job_id'")

        if row_errors:
            result["total_rejected_rows"] += 1
            result["reject_records"].append(
                {"line": index, "id": id, "errors": row_errors}
            )
        else:
            result["total_inserted_rows"] += 1
            valid_rows.append(row)

    return valid_rows, result
