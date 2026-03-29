from flask import Flask, render_template

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
    if search is None:
        return products

    found_items = []
    for item in products:
        if search.lower() in item["name"].lower():
            found_items.append(item)

    if not found_items:
        return "No items found!"
    return found_items

if __name__ == "__main__":
    app.run(debug=True)