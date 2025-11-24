from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, static_url_path = "/static")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/upload", methods=["POST"])
def upload():

    image = request.files.get("image")
    product_id = request.form.get("id")

    print(image)
    print(product_id)

    return render_template("admin.html")

@app.route("/search")
def search():
    conn = sqlite3.connect('computer_store.db')

    q_search = request.args.get('search', '')

    products = conn.execute(f"SELECT id, product_name, price, image FROM products WHERE product_name like '%{q_search}%';").fetchall()
    keys = ["id", "name", "price", "img"]

    products_dicts = []
    for product in products:
        products_dicts.append(dict(zip(keys, product)))

    conn.close()
    return render_template("index.html", products=products_dicts)

@app.route("/")
def index():
    products = [
        {"id": 1, "name": "CPU", "price": 100, "img": "cpu"},
        {"id": 2, "name": "RAM", "price": 50, "img": "ram"}
    ]
    return render_template("index.html", products = products)
