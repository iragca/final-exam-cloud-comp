def grab_product_category(prd_key: str) -> str:
    """
    Get the product category for a given product ID.
    Example:
        >> prd_key: CO-RF-FR-R92B-58
        >> Product ID: CO_RF
    """
    try:
        return prd_key[:5].replace("-", "_")
    except Exception as e:
        print(f"Error retrieving category for product {prd_key}: {e}")
        return None
