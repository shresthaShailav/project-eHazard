import csv

from flask import flash, redirect, render_template, request, session, url_for
from functools import wraps

# a custom decorator for ensuring that the user is logged in
def login_required(f):
    """ Decorate routes to require login

    for documentation see : http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Not Logged in! ")
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def error(top="", bottom="", error_info = "ERROR!"):
    """ Render message as error """
    def escape(s):
        """ Sepcial characters are escaped
        Documentation at : https://github.com/jacebrowning/memegen#special-characters
        """

        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
            ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("error.html", top=escape(top), bottom=escape(bottom), error_info=error_info)


def login_required_as_buyer(f):
    """ Decorate the routes to require login as a buyer """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None or session.get("user_category") != 2:
            return error("You are not allowed to access this page")
        return f(*args, **kwargs)
    return decorated_function


def login_required_as_seller(f):
    """ Decorate the routes to require login as seller """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None or session.get("user_category") != 1:
            return error("You are not allowed to access this page")
        return f(*args, **kwargs)
    return decorated_function
