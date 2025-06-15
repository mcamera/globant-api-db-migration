import logging
from typing import List

from fastapi import HTTPException, UploadFile, status


def get_logger(name: str):
    """Set up logging configuration."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def validate_upload_file(csv_file: UploadFile, max_lines: int = 1000) -> List[str]:
    """Validates the uploaded CSV file.

    Args:
        csv_file (UploadFile): The uploaded CSV file.
        max_lines (int): Maximum number of lines allowed in the CSV file.

    Raises:
        HTTPException: If the file is not provided, is not a CSV, exceeds the maximum number of lines, or is empty.
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

    contents = csv_file.file.read()
    lines = contents.decode("utf-8").splitlines()

    if len(lines) > max_lines:
        logger.error(f"Too many records! Must be less than {max_lines} lines.")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Too many records! Must be less than {max_lines} lines.",
        )

    if len(lines) == 0:
        logger.error("File is empty! Send at least 1 record.")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File is empty! Send at least 1 record.",
        )
