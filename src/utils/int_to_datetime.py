from datetime import datetime


def int_to_datetime(date_int: int) -> datetime.date:
    try:
        result = datetime.strptime(str(date_int), "%Y%m%d").date()
        return result
    except ValueError:
        print(f"Invalid date format: {date_int}. Expected format: YYYYMMDD.")
        return None
