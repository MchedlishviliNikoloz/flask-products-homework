from flask import Flask, render_template, request, redirect, url_for

from validators.product_validator import validate_product, validate_filters
from services.product_service import get_all_products
from services.product_service import add_product as add_product_service
from services.product_service import get_product_by_id as get_product_by_id_service
from services.response_service import make_response

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Phone", "price": 900},
    {"id": 3, "name": "Tablet", "price": 600},
    {"id": 4, "name": "Phone", "price": 1100},
    {"id": 5, "name": "Television", "price": 2600},
    {"id": 6, "name": "Laptop", "price": 1500},
    {"id": 7, "name": "Tablet", "price": 800},
]

@app.route("/")
def index():
    return render_template("index.html", items=products)

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

        result = get_all_products(filters, products)
        message = "Products successfully found" if result else "No product with this name"
        return make_response(filter_validate['success'], data=result, message=message)

    return make_response(filter_validate['success'], message=filter_validate['errors'])

@app.route("/api/products/id/<int:id>")
def get_product_by_id(id: int):
    result = get_product_by_id_service(id, products)
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
        result = get_all_products(filters, products)

    if result is not None:
        return render_template("index.html", items=result)
    return render_template("index.html", errors=filter_validate['errors'])

@app.route("/add-product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        product_add = add_product_service({'name': request.form.get('name'), 'price': request.form.get('price')}, products)
        if not product_add['success']:
            return render_template("add_product.html", errors=product_add['errors'])
        return redirect(url_for("index"))

    return render_template("add_product.html")

@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_product_data(product_id: int):
    data = request.json
    if product_id and isinstance(product_id, int):
        product = get_product_by_id_service(product_id, products)
        name, price = data.get("name"), data.get("price")

        if product is not None:
            for pr in products:
                if product_id == pr["id"]:
                    pr["name"] = name
                    pr["price"] = price

                    return make_response(True, data=products, message=f"Product with id {product_id} successfully updated")

        return make_response(False, message=f"Product with id {product_id} was not found!")

    return make_response(False, message="user id param is not valid, try again!")


@app.route("/api/products/<int:product_id>", methods=["PATCH"])
def partial_update_product_data(product_id: int):
    data = request.json
    if product_id and isinstance(product_id, int):
        product = get_product_by_id_service(product_id, products)
        name, price = data.get("name"), data.get("price")

        if product is not None:
            for pr in products:
                if product_id == pr["id"]:
                    pr["name"] = name if name else product["name"]
                    pr["price"] = price if price else product["price"]

                    return make_response(True, data=products,
                                         message=f"Product with id {product_id} successfully updated")

        return make_response(False, message=f"Product with id {product_id} was not found!")

    return make_response(False, message="user id param is not valid, try again!")


if __name__ == "__main__":
    app.run(debug=True)