def format_revenue(amount: float | int) -> str:
    """#Format revenue as ₱29M, ₱3.2B, etc."""
    if abs(amount) >= 1_000_000_000:
        return f"₱{amount / 1_000_000_000:.1f}B"
    elif abs(amount) >= 1_000_000:
        return f"₱{amount / 1_000_000:.0f}M"
    elif abs(amount) >= 1_000:
        return f"₱{amount / 1_000:.0f}K"
    else:
        return f"₱{amount}"
