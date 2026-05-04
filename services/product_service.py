from validators.product_validator import validate_product
from models.product import Product
from database import db

def get_all_products(filters: dict) -> list:
    query = Product.query

    if "search" in filters:
        query = query.filter(Product.name.like(f"%{filters["search"]}%"))

    if "min_price" in filters:
        query = query.filter(Product.price >= filters["min_price"])

    if "max_price" in filters:
        query = query.filter(Product.price <= filters["max_price"])

    if "limit" in filters:
        query = query.limit(filters["limit"])

    return [p.to_dict() for p in query.all()]

def get_product_by_id(product_id: int):
    return Product.query.get(product_id)

def add_product(new_data: dict):
    product_validate = validate_product(new_data)

    if not product_validate['success']:
        return product_validate

    new_data['price'] = int(new_data['price'])

    product = Product(
        name=new_data["name"],
        price=new_data["price"]
    )
    db.session.add(product)
    db.session.commit()

    return product_validate