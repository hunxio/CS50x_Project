import os
from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        firstName = request.form.get("name")
        lastName = request.form.get("lastname")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        return redirect("/")
        
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect("/")
    return render_template("login.html")