import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from copy import deepcopy

from helpers import apology, login_required

from classes import *

# export API_KEY=pk_baf5acf8b82149dc9fb5e3aece72ca78

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///words.db")


@app.route("/")
@login_required
def index():
    total =  db.execute("SELECT COUNT() FROM stats WHERE id = ?", session["user_id"])
    won =  db.execute("SELECT COUNT() FROM stats WHERE id = ? AND results = 1", session["user_id"])
    tied =  db.execute("SELECT COUNT() FROM stats WHERE id = ? AND results = 0", session["user_id"])
    lost =  db.execute("SELECT COUNT() FROM stats WHERE id = ? AND results = -1", session["user_id"])
    return render_template("index.html", total = total[0]['COUNT()'], won = won[0]['COUNT()'], tied = tied[0]['COUNT()'], lost = lost[0]['COUNT()'])

@app.route("/rules", methods=["GET", "POST"])
@login_required
def rules():
    if request.method == "POST":
        return redirect("/rules")
    else:
        return render_template("rules.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure passwords match
        elif not request.form.get("confirmation") or request.form.get("password") != request.form.get("confirmation"):
            return apology("must confirm matching password", 400)

        # Insert into users table and check if unique
        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))
        except RuntimeError:
            return apology("username taken", 400)
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/start", methods=["GET", "POST"])
@login_required
def start():
    if request.method == "POST":
        global board
        global bag
        global player
        global computer
        board = Board()
        bag = Bag()
        player = Player(bag)
        computer = Computer(bag)
        return redirect("/play")
    else:
        return render_template("start.html")

@app.route("/play", methods=["GET", "POST"])
@login_required
def play():
    global temp_board
    global board
    global player
    global pog
    global computer
    global bag
    if request.method == "POST":
        temp_board = deepcopy(board)
        pog = request.form.get("pog").upper().strip()
        userid = session["user_id"]
        if pog == "PASS":
            return redirect("/check")
        if pog == "END":
            if(player.score > computer.score):
	            db.execute("INSERT INTO stats (id, results) VALUES (?,?)", userid, 1)
            elif(player.score < computer.score):
	            db.execute("INSERT INTO stats (id, results) VALUES (?,?)", userid, -1)
            else:
                db.execute("INSERT INTO stats (id, results) VALUES (?,?)", userid, 0)
            return redirect("/end")
        if temp_board.place_word(pog, player):
            return redirect("/check")
        return redirect("/play")
    else:
        if bag.num_remaining() == 0 and len(player.hand.getHandArr()) == 0:
            return redirect("/end")
        player_score = player.score
        computer_score = computer.score
        return render_template("play.html", board=board.board, hand=player.hand.getHandArr(), player_score=player_score, computer_score=computer_score)

@app.route("/check", methods=["GET", "POST"])
@login_required
def check():
    if request.method == "POST":
        global board
        global temp_baord
        global player
        global pog
        global computer
        # Confirms player's choice (else board will not be updated)
        if request.form.get("submit_button") == "a":
            board.placeword(pog, player)
            # Computer plays here
            if board.place_word_comp(computer.move(board), computer):
                print("Computer has played!")
            else:
                print("Computer has passed!")
        return redirect("/play")
    else:
        return render_template("check.html", board=temp_board.board, hand=player.hand.getHandArr())

@app.route("/end", methods=["GET"])
@login_required
def end():
    if request.method == "GET":
        global player
        global computer
        if player.score < computer.score:
            outcome = "lost"
        elif player.score > computer.score:
            outcome = "won"
        else:
            outcome = "tied"
        return render_template("end.html", outcome=outcome)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


