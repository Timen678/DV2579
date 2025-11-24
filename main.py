from flask import Flask, render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, UserMixin, current_user, login_required
import sqlite3

app = Flask(__name__, static_url_path = "/static")
app.secret_key = "secret"

login_manager = LoginManager(app)
login_manager.login_view = "login"

@app.route("/")
def index():
    products = [
        {"id": 1, "name": "CPU", "price": 100, "img": "cpu"},
        {"id": 2, "name": "RAM", "price": 50, "img": "ram"}
    ]
    return render_template("index.html", products = products)




class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def get_by_id(id_):
        conn = sqlite3.connect("computer_store.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (id_, ))
        row = cursor.fetchone()
        
        if row:
            return User(row[0], row[1], row[2])
        else:
            return None

    @staticmethod
    def get_by_username(username):
        conn = sqlite3.connect("computer_store.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username, ))
        row = cursor.fetchone()
        
        if row:
            return User(row[0], row[1], row[2])
        else:
            return None


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get_by_id(int(user_id))
    except:
        return None


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        user = User.get_by_username(username)
        if not user:
            flash("Wrong credentials")
            return render_template("login.html")
        
        if not check_password_hash(user.password_hash, password):
            flash("Wrong credentials")
            return render_template("login.html")
        
        login_user(user)
        return redirect(url_for("index"))
    
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))