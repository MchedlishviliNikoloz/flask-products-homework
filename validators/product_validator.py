PRODUCT_ERROR_MSGS = {
    "price_not_number": "Price must be a valid number.",
    "price_lower_than_zero": "Price cannot be less than or equal to 0.",
    "short_name": "Name must be at least 2 characters long and cannot be empty."
}
FILTER_ERROR_MSGS = {
    "min_greater_than_max": "Min Price cannot be greater than Max Price.",
    "filter_not_number": "Filter values must be valid numbers."
}

def validate_product(data: dict) -> dict:
    errors = []

    try:
        price = int(data["price"])
        if price <= 0:
            errors.append(PRODUCT_ERROR_MSGS['price_lower_than_zero'])
    except ValueError:
        errors.append(PRODUCT_ERROR_MSGS['price_not_number'])

    if len(data['name']) < 2:
        errors.append(PRODUCT_ERROR_MSGS['short_name'])

    return {
        "success": not errors,
        "errors": errors
    }


def validate_filters(args) -> dict:
    errors = []

    try:
        min_p = int(args["min_price"]) if args.get("min_price") else None
        max_p = int(args["max_price"]) if args.get("max_price") else None
    except ValueError:
        errors.append(FILTER_ERROR_MSGS["filter_not_number"])
        return {"success": False, "errors": errors}

    if min_p is not None and max_p is not None:
        if min_p > max_p:
            errors.append(FILTER_ERROR_MSGS["min_greater_than_max"])

    return {
        "success": not errors,
        "errors": errors
    }