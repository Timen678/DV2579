from flask import Flask, render_template

app = Flask(__name__, static_url_path = "/static")

@app.route("/")
def index():
    products = [
        {"id": 1, "name": "CPU", "price": 100, "img": "cpu"},
        {"id": 2, "name": "RAM", "price": 50, "img": "ram"}
    ]
    return render_template("index.html", products = products)
