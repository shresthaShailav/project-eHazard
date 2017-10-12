from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from flask_sqlalchemy import SQLAlchemy

from helpers import *

# configure application
app = Flask(__name__)
app.debug = True

# turn off SQLAlchemy event system
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# ensure that the responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response



# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



# configure database with sqlalchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    """ !!! 
        loads the guest index with the option to login if the user is not logged in, Register, or view the about and contact page
        If the user is already logged in then it displays the respective index pages for the user
    """
    return render_template("seller_index.html")

@app.route("/check")
def check():
    tables = db.engine.execute('SELECT name FROM sqlite_master WHERE type = "table";')
    print(tables)
    session['user_category'] = 3
    return render_template("check.html", tables=tables)

@app.route("/error_code")
def error_code():
    return error("AN example", "of error",
            error_info="THis is an error")

@app.route("/login", methods=["GET", "POST"])
def login():
    """ !!! """
    """ Logs the user into the system 
        If logged in as a buyer, loads the buyer index
        If logged in as a seller loads the seller index
        Else shows error"""
    session.clear()

    if request.method == "POST":
        return error("Working on it! ", error_info="Making the form")
    else:
        return render_template("login.html")
    

@app.route("/register", methods=["GET", "POST"])
def register():
    """ !!! """
    """ Registers the user by adding their credentials into the database """
    if request.method == "POST":
        return error("Working on it! ", error_info="Not added to database")
    else:
        return render_template("register.html")
    

@app.route("/about", methods=["GET"])
def about():
    """ !!! """
    """ Just loads the about page 
        BUT the about page inherits different pages depending on the login in status
        If logged in as seller, inherits the seller index
        If logged in as buyer, inherits the buyer index
        If Guest inherits the guest index
        Will probably have to be implemented with Jinja at the front 
    """
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    """ !!! """
    """ Just loads the contacts page 
        BUT the contact page inherits different pages depending on the login in status
        If logged in as seller, inherits the seller index
        If logged in as buyer, inherits the buyer index
        If Guest inherits the guest index
        Will probably have to be implemented with Jinja at the front 
    """
    return render_template("contact.html")


