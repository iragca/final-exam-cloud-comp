def int_to_datetime_str(date_int: int) -> str:
    date_str = str(date_int)
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
