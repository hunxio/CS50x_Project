import os
import sqlite3
import re
import argon2
from flask import Flask, render_template, redirect, request, session
from flask_session import Session

from personaldefs import returnErrorMessage

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False  # The session will have a default lifetime which will expire 
app.config["SESSION_TYPE"] = "filesystem" #It will store the session in the filesystem
Session(app)

# Homepage #
@app.route("/")
def home():
    return render_template("homepage.html")


# FIXME: Test page for successful login, not established a session yet
@app.route("/loginok")
def loginok():
    return render_template("loginok.html")


# Successfully registering an account redirects the user here #
@app.route("/success")
def success():
    return render_template("success.html")


# Whenever one of the validation errors occurs, the user is redirected to this page #
@app.route("/errorpage")
def errorpage():
    return render_template("errorpage.html")


# Signup page #
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Database creation and update #
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, lastname TEXT NOT NULL, email TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL);"
        )

        # Getting data from inputs and checking for errors/duplicates in DB #

        # NAME VALIDATION #
        name = request.form.get("name")
        if not name:
            return returnErrorMessage(con, "errorpage.html", "Name was missing")

        # LAST NAME VALIDATION #
        lastName = request.form.get("lastname")
        if not lastName:
            return returnErrorMessage(con, "errorpage.html", "Last name was missing")

        # EMAIL VALIDATION #
        email = request.form.get("email")
        if not email:
            return returnErrorMessage(con, "errorpage.html", "Email was missing")

        emailValidation = re.search(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$", email)
        if emailValidation is None:
            return returnErrorMessage(con, "errorpage.html", "Email does not match")

        emailCur = cur.execute("SELECT email FROM users;")
        emailList = emailCur.fetchall()
        for _ in range(len(emailList)):
            if email == emailList[_][0]:
                return returnErrorMessage(con, "errorpage.html", "Email already exists")

        # USERNAME VALIDATION #
        username = request.form.get("username")
        if not username:
            return returnErrorMessage(con, "errorpage.html", "Username was missing")

        usernameCur = cur.execute("SELECT username FROM users;")
        usernameList = usernameCur.fetchall()
        for _ in range(len(usernameList)):
            if username == usernameList[_][0]:
                return returnErrorMessage(
                    con, "errorpage.html", "Username already exists"
                )

        # PASSWORD VALIDATION #
        password = request.form.get("password")
        if not password:
            return returnErrorMessage(con, "errorpage.html", "Password was missing")

        if len(password) < 8 or len(password) > 16:
            return returnErrorMessage(
                con,
                "errorpage.html",
                "Password must be between 8 and 16 characters long",
            )

        passwordValidation = re.search(
            r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,16}", password
        )
        if passwordValidation is None:
            return returnErrorMessage(
                con, "errorpage.html", "Password format is invalid"
            )

        # Password hash and salt with argon2 #
        hasher = argon2.PasswordHasher()
        hashPassword = hasher.hash(password)

        # Update database #
        cur.execute(
            "INSERT INTO users (name, lastname, email, username, password) VALUES (?, ?, ?, ?, ?);",
            (name, lastName, email, username, hashPassword),
        )
        con.commit()
        con.close()
        return redirect("success")
    return render_template("signup.html")


# Login page #
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Variables #
        passwordFound = None
        usernameFound = None

        # Database connection #
        con = sqlite3.connect("database.db")
        cur = con.cursor()

        # USERNAME VALIDATION #
        session["username"] = request.form.get("username")
        username = session["username"]
        if not username:
            return returnErrorMessage(con, "errorpage.html", "Username was missing")

        usernameCur = cur.execute("SELECT username FROM users;")
        usernameList = usernameCur.fetchall()
        for _ in range(len(usernameList)):
            if username == usernameList[_][0]:
                usernameFound = usernameList[_][0]

        # PASSWORD VALIDATION #
        password = request.form.get("password")
        if not password:
            return returnErrorMessage(con, "errorpage.html", "Password was missing")

        # Retrieve password from DB and attribuite it to passwordFound#
        passwordCur = cur.execute(
            "SELECT password FROM users WHERE username = ?;", (usernameFound,)
        )
        passwordOfUser = passwordCur.fetchone()
        passwordFound = passwordOfUser[0]
        if passwordFound is None or usernameFound is None:
            return returnErrorMessage(
                con, "errorpage.html", "Invalid username or password"
            )

        # Password hash and salt with argon2 for validation #
        hasher = argon2.PasswordHasher()
        hashPassword = hasher.hash(password)

        # Verifying password #
        try:
            hasher.verify(passwordFound, password)
            con.close()
            return redirect("/loginok")
        except argon2.exceptions.VerifyMismatchError:
            return returnErrorMessage(con, "errorpage.html", "Password does not exist")
    return render_template("login.html")
