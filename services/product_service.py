from validators.product_validator import validate_product


def get_all_products(filters: dict, products: list) -> list:
    filtered_products = products

    if "search" in filters:
        filtered_products = [p for p in filtered_products if filters['search'].lower() in p['name'].lower()]

    if "min_price" in filters:
        filtered_products = [p for p in filtered_products if filters['min_price'] <= p['price']]

    if "max_price" in filters:
        filtered_products = [p for p in filtered_products if filters['max_price'] >= p['price']]

    if "limit" in filters:
        filtered_products = filtered_products[:int(filters["limit"])]

    return filtered_products

def get_product_by_id(product_id: int, products: list):
    for product in products:
        if product_id == product['id']:
            return product
    return None

def add_product(new_data: dict, existing_data: list):
    product_validate = validate_product(new_data)

    if not product_validate['success']:
        return product_validate

    new_data['id'] = len(existing_data) + 1
    new_data['price'] = int(new_data['price'])
    existing_data.append(new_data)
    return product_validate