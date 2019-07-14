from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(500))

    def __init__(self, title, content):
        self.title = title
        self.content = content

titles = []
contents = []

@app.route("/", methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        title = request.form['title']
        content = reqeuest.form['content']
        titles.append(title)
        contents.append(contents)

    return render_template("index.html", title="Build A Blog", titles=titles, contents=contents)

@app.route("/form")
def submit_form():
    return render_template("form.html")

@app.route("/display")
def display_form():
    return render_template("display.html")

if __name__ == '__main__':
    app.run()