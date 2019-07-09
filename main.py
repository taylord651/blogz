from flask import Flask, request, redirect, render_template
import cgi
import os

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def display_blog():
    return render_template("index.html")

@app.route("/form")
def submit_form():
    return render_template("form.html")

@app.route("/display")
def display_form():
    return render_template("display.html")

app.run()