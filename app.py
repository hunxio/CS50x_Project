import os
import sqlite3
import re
import argon2
from flask import Flask, render_template, redirect, request

app = Flask(__name__)

# Homepage #
@app.route("/")
def home():
    return render_template("homepage.html")

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
        # Error code variable #
        code_error = None

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
            code_error = "Name was missing"
            return render_template("errorpage.html", message=code_error)

        # LAST NAME VALIDATION #
        lastName = request.form.get("lastname")
        if not lastName:
            code_error = "Last Name was missing"
            return render_template("errorpage.html", message=code_error)

        # EMAIL VALIDATION #
        email = request.form.get("email")
        emailCur = cur.execute("SELECT email FROM users;")
        emailList = emailCur.fetchall()
        emailValidation = re.search(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$", email)
        if not email:
            code_error = "Email was missing"
            return render_template("errorpage.html", message=code_error)
        elif emailValidation is None:
            code_error = "Invalid email address"
            return render_template("errorpage.html", message=code_error)
        for _ in range(len(emailList)):
            if email == emailList[_][0]:
                code_error = "Email already exists"
                return render_template("errorpage.html", message=code_error)

        # USERNAME VALIDATION #
        username = request.form.get("username")
        usernameCur = cur.execute("SELECT username FROM users;")
        usernameList = usernameCur.fetchall()
        if not username:
            code_error = "Username was missing"
            return render_template("errorpage.html", message=code_error)
        for _ in range(len(usernameList)):
            if username == usernameList[_][0]:
                code_error = "Username already exists"
                return render_template("errorpage.html", message=code_error)

        # PASSWORD VALIDATION #
        password = request.form.get("password")
        passwordValidation = re.search(
            r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,16}", password
        )
        if not password:
            code_error = "Password was missing"
            return render_template("errorpage.html", message=code_error)
        elif len(password) < 8 or len(password) > 16:
            code_error = "Invalid password length"
            return render_template("errorpage.html", message=code_error)
        elif passwordValidation is None:
            code_error = "Password not valid"
            return render_template("errorpage.html", message=code_error)

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
        username = request.form.get("username")
        if not username:
            code_error = "Username was missing"
            return render_template("errorpage.html", message=code_error)
        password = request.form.get("password")
        if not password:
            code_error = "Password was missing"
            return render_template("errorpage.html", message=code_error)
        return redirect("/")
    return render_template("login.html")
