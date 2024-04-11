import os

import sqlite3
from flask import Flask, render_template, redirect, request
import re
import argon2

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/errorpage")
def errorpage():
    return render_template("errorpage.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
         # Database creation and update #
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, lastname TEXT NOT NULL, email TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL);")
        
        # TODO: Add more controls to check if the username and/or email already exists.abs

        # Getting data from inputs and checking for errors/duplicates in DB #
        name = request.form.get("name")
        if not name:
            code_error = "Name was missing"
            return render_template("errorpage.html", message=code_error)
        lastName = request.form.get("lastname")
        if not lastName:
            code_error = "Last Name was missing"
            return render_template("errorpage.html", message=code_error)
        email = request.form.get("email")
        emailValidation = re.search(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$", email)
        if not email:
            code_error = "Email was missing"
            return render_template("errorpage.html", message=code_error)
        elif emailValidation is None:
            code_error = "Invalid email address"
            return render_template("errorpage.html", message=code_error)
        username = request.form.get("username")
        if not username:
            code_error = "Username was missing"
            return render_template("errorpage.html", message=code_error)
        password = request.form.get("password")
        passwordValidation = re.search(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,16}", password)
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
        cur.execute("INSERT INTO users (name, lastname, email, username, password) VALUES (?, ?, ?, ?, ?);", (name, lastName, email, username, hashPassword))
        con.commit()
        con.close()
        return redirect("/")
    return render_template("signup.html")

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