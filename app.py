from flask import Flask, render_template, request, redirect, url_for

from validators.product_validator import validate_product, validate_filters
from services.product_service import get_all_products
from services.product_service import add_product as add_product_service
from services.product_service import get_product_by_id as get_product_by_id_service
from services.response_service import make_response
from database import db
from models.product import Product

app = Flask(__name__)

# products = [
#     {"id": 1, "name": "Laptop", "price": 1200},
#     {"id": 2, "name": "Phone", "price": 900},
#     {"id": 3, "name": "Tablet", "price": 600},
#     {"id": 4, "name": "Phone", "price": 1100},
#     {"id": 5, "name": "Television", "price": 2600},
#     {"id": 6, "name": "Laptop", "price": 1500},
#     {"id": 7, "name": "Tablet", "price": 800},
# ]
DB_PATH = "products.db"

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html", items=Product.query.all())

@app.route("/api/products")
@app.route("/api/products/<search>")
def get_products(search: str = None):
    filter_validate = validate_filters(request.args)
    if filter_validate['success']:
        filters = {}
        if search:
            filters['search'] = search
        if request.args.get("min_price"):
            filters['min_price'] = int(request.args.get("min_price"))
        if request.args.get("max_price"):
            filters['max_price'] = int(request.args.get("max_price"))
        if request.args.get("limit"):
            filters['limit'] = int(request.args.get("limit"))

        result = get_all_products(filters)
        message = "Products successfully found" if result else "No product with this name"
        return make_response(filter_validate['success'], data=result, message=message)

    return make_response(filter_validate['success'], message=filter_validate['errors'])

@app.route("/api/products/id/<int:id>")
def get_product_by_id(id: int):
    result = get_product_by_id_service(id)
    if result is not None:
        return make_response(True, data=result, message=f"Found product with ID {id}")
    return make_response(False, message=f"Product not found with ID {id}")

@app.route("/products")
def get_products_page():
    filter_validate = validate_filters(request.args)
    result = None
    if filter_validate['success']:
        filters = {}
        if request.args.get("min_price"):
            filters['min_price'] = int(request.args.get("min_price"))
        if request.args.get("max_price"):
            filters['max_price'] = int(request.args.get("max_price"))
        if request.args.get("limit"):
            filters['limit'] = int(request.args.get("limit"))
        result = get_all_products(filters)

    if result is not None:
        return render_template("index.html", items=result)
    return render_template("index.html", errors=filter_validate['errors'])

@app.route("/add-product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        product_add = add_product_service({'name': request.form.get('name'), 'price': request.form.get('price')})
        if not product_add['success']:
            return render_template("add_product.html", errors=product_add['errors'])
        return redirect(url_for("index"))

    return render_template("add_product.html")

@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_product_data(product_id: int):
    data = request.json
    if product_id and isinstance(product_id, int):
        product = get_product_by_id_service(product_id)
        name, price = data.get("name"), data.get("price")

        if product is not None:
            product.name = name
            product.price = price
            db.session.commit()
            return make_response(True, data=product.to_dict(), message=f"Product with id {product_id} successfully updated")

        return make_response(False, message=f"Product with id {product_id} was not found!")

    return make_response(False, message="user id param is not valid, try again!")


@app.route("/api/products/<int:product_id>", methods=["PATCH"])
def partial_update_product_data(product_id: int):
    data = request.json
    if product_id and isinstance(product_id, int):
        product = get_product_by_id_service(product_id)
        name, price = data.get("name"), data.get("price")

        if product is not None:
            product.name = name if name else product.name
            product.price = price if price else product.price
            db.session.commit()
            return make_response(True, data=product.to_dict(), message=f"Product with id {product_id} successfully updated")

        return make_response(False, message=f"Product with id {product_id} was not found!")

    return make_response(False, message="user id param is not valid, try again!")


@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id: int):
    if product_id and isinstance(product_id, int):
        product = get_product_by_id_service(product_id)

        if product is not None:
            db.session.delete(product)
            db.session.commit()
            return make_response(True, message=f"Product with id {product_id} successfully deleted")

        return make_response(False, message=f"Product with id {product_id} was not found!")

    return make_response(False, message="user id param is not valid, try again!")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)