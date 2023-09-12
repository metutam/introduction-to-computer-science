import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/account", methods=["GET", "POST"])
@login_required
def accout():
    """Allow users to change their passwords"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Take the user input
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # Ensure current password was entered
        if not current_password:
            return apology("missing current password")
        # Ensure new password was entered
        elif not new_password:
            return apology("missing new password")
        # Ensure confirmation was entered
        elif not confirmation:
            return apology("missing confirm new password")

        # Ensure the passwords match
        if new_password != confirmation:
            return apology("passwords do not match")

        # Query database for hash
        rows = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])

        # Ensure the user's password and entered current password match
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("current_password")
        ):
            return apology("passwords do not match")

        # Hash the user’s password with generate_password_hash
        password_hash = generate_password_hash(request.form.get("new_password"))

        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?", password_hash, session["user_id"]
        )

        # Redirect user to home page
        return redirect("/")

    return render_template("account.html")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Query database for which stocks the user owns, the numbers of shares owned
    stock = db.execute(
        "SELECT id, name, SUM(price), SUM(shares), symbol FROM stocks WHERE user_id = ? GROUP BY symbol",
        session["user_id"],
    )

    # Query database for id
    rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

    # Determine how much cash the user currently has
    cash = rows[0]["cash"]

    # Determine the current price of each stock
    current_price = {}
    for item in stock:
        share = lookup(item["symbol"])
        current_price[item["id"]] = share["price"]

    # Determine total value of each holding (i.e., shares times price)
    total_value = cash
    for item in stock:
        total_value += item["SUM(shares)"] * current_price[item["id"]]

    return render_template(
        "index.html",
        stock=stock,
        cash=cash,
        current_price=current_price,
        total_value=total_value,
        usd=usd,
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Take the user input
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure symbol was submitted
        if not symbol:
            return apology("missing symbol")

        # Ensure shares is a positive integer
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be a positive integer")

        if shares <= 0:
            return apology("shares must be a positive integer")

        # lookup function returns a stock quote for a company in the form of a dict
        stock = lookup(symbol)

        if not stock:
            return apology("the symbol does not exist")

        # Query database for id
        rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        # Determine how much cash the user currently has
        cash = rows[0]["cash"]

        stock_name = stock["name"]
        stock_price = stock["price"]
        total_price = stock_price * shares

        if cash < total_price:
            return apology("cannot afford the shares")

        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            cash - total_price,
            session["user_id"],
        )
        db.execute(
            "INSERT INTO stocks (name, shares, price, type, symbol, user_id) VALUES (?, ?, ?, ?, ?, ?)",
            stock_name,
            shares,
            stock_price,
            "buy",
            symbol,
            session["user_id"],
        )

        # Redirect user to home page
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    stock = db.execute(
        "SELECT symbol, type, shares, price, time FROM stocks WHERE user_id = ?",
        session["user_id"],
    )

    return render_template("history.html", stock=stock, usd=usd)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST
    if request.method == "POST":
        # Take the user input
        symbol = request.form.get("symbol")

        # Ensure symbol was entered
        if not symbol:
            return apology("missing symbol")

        # lookup function returns a stock quote for a company in the form of a dict
        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol")

        worth = usd(stock["price"])
        return render_template("quoted.html", stock=stock, worth=worth)

    # User reached route via GET
    elif request.method == "GET":
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Take the user input
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was entered
        if not username:
            return apology("missing username")
        # Ensure password was entered
        elif not password:
            return apology("missing password")
        # Ensure confirmation was entered
        elif not confirmation:
            return apology("missing confirm password")

        # Ensure the passwords match
        if password != confirmation:
            return apology("passwords do not match")

        # Hash the user’s password with generate_password_hash
        password_hash = generate_password_hash(request.form.get("password"))

        try:
            # insert the new user into users
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username,
                password_hash,
            )
            # Redirect user to home page
            return redirect("/")
        except:
            # Render an apology if the username already exists
            return apology("username already exists")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Take the user input
        symbol = request.form.get("symbol")

        # Ensure user selects a stock
        if not request.form.get("symbol"):
            return apology("user fails to select a stock")

        # Ensure shares is a positive integer
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be a positive integer")

        # Ensure that shares is a positive integer
        if shares <= 0:
            return apology("shares must be a positive integer")

        # Ensure user owns that many shares of the stock
        owned = db.execute(
            "SELECT shares FROM stocks WHERE user_id = ? AND symbol = ? GROUP BY symbol",
            session["user_id"],
            symbol,
        )
        if owned[0]["shares"] < shares:
            return apology("user does not own that many shares of the stock")

        stock = lookup(symbol)
        stock_name = stock["name"]
        stock_price = stock["price"]
        total_price = stock_price * shares

        # Query database for id
        rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        # Determine how much cash the user currently has
        cash = rows[0]["cash"]

        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            cash + total_price,
            session["user_id"],
        )
        db.execute(
            "INSERT INTO stocks (name, shares, price, type, symbol, user_id) VALUES (?, ?, ?, ?, ?, ?)",
            stock_name,
            -shares,
            stock_price,
            "sell",
            symbol,
            session["user_id"],
        )

        # Redirect user to home page
        return redirect("/")

    symbols = db.execute(
        "SELECT symbol FROM stocks WHERE user_id = ? GROUP BY symbol",
        session["user_id"],
    )
    return render_template("sell.html", symbols=symbols)
