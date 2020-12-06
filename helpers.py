import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from random import randint


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def random_tuples(sequence, n):
    # Generates n random tuple with coords between 0 and 14 that is not already in the list sequence
    count = 0
    while True:
        if count == n:
            break
        x = randint(0,14)
        y = randint(0,14)
        if (x,y) in sequence or (x,y) == (7,7):
            continue
        else:
            sequence.append((x,y))
            count += 1

