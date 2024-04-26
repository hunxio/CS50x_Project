import os

import sqlite3
import re
import argon2
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from utils import ErrorTemplate, ErrorConnection, acquireSessionEmail, hashPassword, movieapi

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = (
    False  # The session will have a default lifetime which will expire
)
app.config["SESSION_TYPE"] = "filesystem"  # It will store the session in the filesystem
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Homepage #
@app.route("/")
def home():
    if not session.get("email"):
        return render_template("homepage.html")

    con = sqlite3.connect("database.db")
    cur = con.cursor()
    userUsername = acquireSessionEmail(cur)
    return render_template("homepage.html", username=userUsername)


@app.route("/layout")
def index():
    if not session.get("username"):
        return redirect("/homepage")
    return render_template("layout.html")


# Log Out #
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


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
            return ErrorConnection(con, "Name was missing")

        # LAST NAME VALIDATION #
        lastName = request.form.get("lastname")
        if not lastName:
            return ErrorConnection(con, "Last name was missing")

        # EMAIL VALIDATION #
        email = request.form.get("email")
        if not email:
            return ErrorConnection(con, "Email was missing")

        emailValidation = re.search(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$", email)
        if emailValidation is None:
            return ErrorConnection(con, "Email does not match")

        emailCur = cur.execute("SELECT email FROM users;")
        emailList = emailCur.fetchall()
        for _ in range(len(emailList)):
            if email == emailList[_][0]:
                return ErrorConnection(con, "Email already exists")

        # USERNAME VALIDATION #
        username = request.form.get("username")
        if not username:
            return ErrorConnection(con, "Username was missing")
        if len(username) > 10 or len(username) < 4:
            session.clear()
            return ErrorConnection(
                con,
                "Username must be between 4 and 10 characters long, plese try again.",
            )

        usernameCur = cur.execute("SELECT username FROM users;")
        usernameList = usernameCur.fetchall()
        for _ in range(len(usernameList)):
            if username == usernameList[_][0]:
                return ErrorConnection(con, "Username already exists")

        # PASSWORD VALIDATION #
        password = request.form.get("password")
        if not password:
            return ErrorConnection(con, "Password was missing")

        if len(password) < 8 or len(password) > 16:
            return ErrorConnection(
                con,
                "Password must be between 8 and 16 characters long",
            )

        passwordValidation = re.search(
            r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,16}", password
        )
        if passwordValidation is None:
            return ErrorConnection(con, "Password format is invalid")

        # Password hash and salt with argon2 #
        hashedPassword = hashPassword(password)

        # Update database #
        cur.execute(
            "INSERT INTO users (name, lastname, email, username, password) VALUES (?, ?, ?, ?, ?);",
            (name, lastName, email, username, hashedPassword),
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
        emailFound = None
        passwordFound = None

        # Database connection #
        con = sqlite3.connect("database.db")
        cur = con.cursor()

        # USERNAME VALIDATION #
        session["email"] = request.form.get("email")
        email = session["email"]
        if not email:
            session.clear()
            return ErrorConnection(con, "Email was missing")

        emailCur = cur.execute("SELECT email FROM users;")
        emailList = emailCur.fetchall()
        for _ in range(len(emailList)):
            if email == emailList[_][0]:
                emailFound = emailList[_][0]

        # PASSWORD VALIDATION #
        password = request.form.get("password")
        if not password:
            session.clear()
            return ErrorConnection(con, "Password was missing")

        # Retrieve password from DB and attribuite it to passwordFound #
        passwordCur = cur.execute(
            "SELECT password FROM users WHERE email = ?;", (emailFound,)
        )
        try:
            passwordOfUser = passwordCur.fetchone()
            passwordFound = passwordOfUser[0]
        except TypeError:
            session.clear()
            return ErrorConnection(con, "Invalid email or password")

        # Password hash and salt with argon2 for validation #
        hasher = argon2.PasswordHasher()
        hashPassword = hasher.hash(password)

        # Verifying password #
        try:
            hasher.verify(passwordFound, password)
            con.close()
            return redirect("/")
        except argon2.exceptions.VerifyMismatchError:
            session.clear()
            return ErrorConnection(con, "Password does not match ")
    return render_template("login.html")


@app.route("/settings", methods=["GET", "POST"])
def setting():
    if not session.get("email"):
        return ErrorTemplate("You are not logged in")

    con = sqlite3.connect("database.db")
    cur = con.cursor()
    userUsername = acquireSessionEmail(cur)
    return render_template("settings.html", username=userUsername)


@app.route("/changepassword", methods=["GET", "POST"])
def changePassword():
    # Database connection #
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    # If user not logged in, it will be redirected to error page #
    if not session.get("email"):
        return ErrorConnection(con, "You are not logged in")

    if request.method == "POST":
        # Session Username #
        sessionUsername = acquireSessionEmail(cur)

        # NEW PASSWORD VALIDATION #
        newPassword = request.form.get("newPassword")
        if not newPassword:
            return ErrorConnection(con, "No password provided")
        if len(newPassword) < 8 or len(newPassword) > 16:
            return ErrorConnection(
                con,
                "The new password must be between 8 and 16 characters long",
            )
        # NEW PASSWORD PATTERN VALIDATION #
        newPasswordValidation = re.search(
            r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,16}", newPassword
        )
        if newPasswordValidation is None:
            return ErrorConnection(con, "Password format is invalid")

        # CONFIRM PASSWORD VALIDATION #
        confirmPassword = request.form.get("confirmPassword")
        if not confirmPassword:
            return ErrorConnection(con, "No password provided for confirmation")
        if newPassword != confirmPassword:
            return ErrorConnection(con, "Passwords does not match")

        # Password hash and salt with argon2 #
        updatedPassword = hashPassword(newPassword)

        # Update database with new hashed password #
        newPasswordUpdate = cur.execute(
            "UPDATE users SET password = ? WHERE username = ?;",
            (
                updatedPassword,
                sessionUsername,
            ),
        )
        con.commit()
        con.close()
        return redirect("success")

    userUsername = acquireSessionEmail(cur)
    con.close()
    return render_template("changepassword.html", username=userUsername)


@app.route("/changeusername", methods=["GET", "POST"])
def changeusername():
    # Database connection #
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    # If user not logged in, it will be redirected to error page #
    if not session.get("email"):
        return ErrorConnection(con, "You are not logged in")

    if request.method == "POST":
        # Session Username #
        sessionUsername = acquireSessionEmail(cur)

        # USERNAME VALIDATION #
        newUsername = request.form.get("newUsername")
        if not newUsername:
            return ErrorConnection(con, "No username provided")
        if len(newUsername) > 10 or len(newUsername) < 4:
            return ErrorConnection(
                con, "The new username must be between 4 and 10 characters long"
            )
        # CONFIRM USERNAME VALIDATION #
        confirmUsername = request.form.get("confirmUsername")
        if not confirmUsername:
            return ErrorConnection(con, "No username provided for confirmation")
        if newUsername != confirmUsername:
            return ErrorConnection(con, "Username does not match")

        # CHECKING IF USERNAME ALREADY EXISTS #
        usernameCur = cur.execute("SELECT username FROM users;")
        usernameList = usernameCur.fetchall()
        for _ in range(len(usernameList)):
            if newUsername == usernameList[_][0]:
                return ErrorConnection(con, "Username already exists")
        # Update username if it doesn't already exist #
        updateUsername = cur.execute(
            "UPDATE users SET username = ? WHERE username = ?;",
            (newUsername, sessionUsername),
        )
        con.commit()
        con.close()
        return redirect("success")

    userUsername = acquireSessionEmail(cur)
    con.close()
    return render_template("changeusername.html", username=userUsername)

@app.route("/gallery", methods=["GET"])
def gallery():
        # Database connection #
        con = sqlite3.connect("database.db")
        cur = con.cursor()

        # If user not logged in, it will be redirected to error page #
        if not session.get("email"):
            return ErrorConnection(con, "You are not logged in")

        test = movieapi(300001)
        return render_template("gallery.html", test=test)