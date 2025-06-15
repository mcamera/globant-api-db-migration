from fastapi import HTTPException, UploadFile, status
from utils import get_logger


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
