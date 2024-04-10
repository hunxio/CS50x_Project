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
            return redirect("/errorpage")
        email = request.form.get("email")
        if not email:
            return redirect("/errorpage")
        username = request.form.get("username")
        if not username:
            return redirect("/errorpage")
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