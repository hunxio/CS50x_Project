import os
import sqlite3
from flask import Flask, render_template, redirect, request

# It will close the database connection and return an error page #
def ErrorConnection(con, code_error):
    con.close()
    return render_template("errorpage.html", message=code_error)

# Basic template for error page, in case no access to the database and user did not login #
def ErrorTemplate(code_error):
    return render_template("errorpage.html", message=code_error)