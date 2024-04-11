import os

import sqlite3
from flask import Flask, render_template, redirect, request
import re

app = Flask(__name__)

con = sqlite3.connect("database.db")
cur = con.cursor()

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/errorpage")
def errorpage():
    return render_template("errorpage.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
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
            return redirect("/errorpage")
        elif len(password) < 8 or len(password) > 16:
            return redirect("/errorpage")
        elif passwordValidation is None:
            return redirect("/errorpage")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        return redirect("/")
    return render_template("login.html")