import os
import sqlite3
from flask import Flask, render_template, redirect, request

def returnErrorMessage(con, page, code_error):
    con.close()
    return render_template(page, message=code_error)