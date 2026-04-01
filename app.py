from flask import Flask, render_template, request, redirect, url_for

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
    result = products
    min_price, max_price = request.args.get("min_price"), request.args.get("max_price")
    limit = request.args.get("limit")

    if search is not None:
        result = [item for item in result if search.lower() in item['name'].lower()]

    if min_price:
        result = [item for item in result if int(min_price) <= item['price']]

    if max_price:
        result = [item for item in result if int(max_price) >= item['price']]

    if limit:
        result = result[:int(limit)]

    return result

@app.route("/api/products/id/<int:id>")
def get_product_by_id(id: int):
    for item in products:
        if id == item['id']:
            return item
    return {"error": "Product not found"}

@app.route("/products")
def get_products_page():
    min_price, max_price = request.args.get("min_price"), request.args.get("max_price")
    result = products
    if min_price:
        result = [item for item in result if int(min_price) <= item['price']]

    if max_price:
        result = [item for item in result if int(max_price) >= item['price']]

    return render_template("index.html", items=result)

@app.route("/add-product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        p_name = request.form.get('name')
        p_price = request.form.get('price')
        p_id = len(products) + 1
        products.append({
            'id': p_id,
            'name': p_name,
            'price': int(p_price)
        })
        return redirect(url_for("index"))

    return render_template("add_product.html")

if __name__ == "__main__":
    app.run(debug=True)