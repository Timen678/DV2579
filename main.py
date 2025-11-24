from flask import Flask, render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, UserMixin, current_user, login_required
import sqlite3
import logging
import os
import uuid

# Logging
db_logger = logging.getLogger("sqlite_trace")
db_logger.setLevel(logging.DEBUG)
db_handler = logging.FileHandler("database.log")
db_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
db_handler.setFormatter(formatter)
db_logger.addHandler(db_handler)



def sql_trace(statement):
    db_logger.debug("SQL TRACE: %s", statement)

app = Flask(__name__, static_url_path = "/static")
app.secret_key = "secret"

# UPLOAD DIRECTORY
UPLOAD_FOLDER = "static/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/upload", methods=["POST"])
def upload():
    conn = sqlite3.connect('computer_store.db')
    conn.set_trace_callback(sql_trace)

    image = request.files.get("image")
    product_id = request.form.get("product_id")

    # Check if uploaded image name is ok
    if not image or image.filename == '':
        conn.close()
        return ("no file selected", 400)

    
    # Check if supplied product id is valid
    old_filename = conn.execute('SELECT image FROM products WHERE id = ?', (product_id,)).fetchone()
    if old_filename is None:
        conn.close()
        return ('Not a valid product ID')


    old_filepath = os.path.join(app.config["UPLOAD_FOLDER"], old_filename[0])
    new_filepath = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)

    # Save new image
    try:
        image.save(new_filepath)
    except:
        conn.close()
        return ('Internal error', 500)


    # Change aspect ratio of image
    abs_new_filepath = os.path.abspath(new_filepath)
    temp_file = f"{str(uuid.uuid4())}.jpg"
    print(abs_new_filepath)
    os.system(f"ffmpeg -i {abs_new_filepath} -vf scale=200:200 {temp_file} -y")
    os.remove(f"{abs_new_filepath}")
    os.rename(f"{temp_file}", abs_new_filepath)
    
    # Update product image
    try:
        conn.execute("UPDATE products SET image = ? WHERE id = ?", (image.filename, product_id))
    except:
        conn.close()
        return ('Internal error', 500)

    # Remove old file
    try:
        os.remove(old_filepath)
    except:
        conn.close()
        return ('internal error', 500)
    
    conn.commit()
    conn.close()
    return render_template("admin.html")

login_manager = LoginManager(app)
login_manager.login_view = "login"

@app.route("/")
def index():
    conn = sqlite3.connect('computer_store.db')
    conn.set_trace_callback(sql_trace)

    q_search = request.args.get('search', '')

    products = conn.execute(f"SELECT id, product_name, price, image FROM products WHERE product_name like '%{q_search}%';").fetchall()
    keys = ["id", "name", "price", "img"]

    products_dicts = []
    for product in products:
        products_dicts.append(dict(zip(keys, product)))

    conn.close()
    return render_template("index.html", products=products_dicts)


class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def get_by_id(id_):
        conn = sqlite3.connect("computer_store.db")
        # conn.set_trace_callback(sql_trace)
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
        conn.set_trace_callback(sql_trace)
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