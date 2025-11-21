from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    products = [
        {"id": 1, "name": "Computer part 1"},
        {"id": 2, "name": "Computer part 2"}
    ]
    return render_template("index.html", products = products)
