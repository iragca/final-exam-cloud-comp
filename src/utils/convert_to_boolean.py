def convert_to_boolean(text: str) -> bool:
    """Convert text to boolean."""
    if text.lower() in ["yes", "true", "1"]:
        return True
    elif text.lower() in ["no", "false", "0"]:
        return False
    else:
        raise ValueError(f"Cannot convert {text} to boolean")
