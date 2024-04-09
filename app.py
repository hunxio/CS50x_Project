import os
from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        return redirect("homepage.html")
    return render_template("signup.html")