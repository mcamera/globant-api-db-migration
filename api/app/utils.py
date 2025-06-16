import logging


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


def fix_datetime(csv_rows: list[tuple]) -> list[tuple]:
    """Fix datetime format in the rows tuples.

    I.e., convert '2023-10-01T12:00:00Z' to '2023-10-01 12:00:00'.

    Args:
        csv_rows (list[tuple]): List of tuples containing data from the CSV file.

    Returns:
        list[tuple]: List of tuples with fixed datetime format.
    """
    fixed_rows = []
    for row in csv_rows:
        fixed_row = []
        for item in row:
            if isinstance(item, str) and "T" in item and "Z" in item:
                item = item.replace("T", " ").replace("Z", "")
            fixed_row.append(item)
        fixed_rows.append(tuple(fixed_row))

    return fixed_rows
