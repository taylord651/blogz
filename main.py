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
    author = db.Column(db.String(120))
    date = db.Column(db.String(120))

    def __init__(self, title, author, date, content):
        self.title = title
        self.author = author
        self.date = date
        self.content = content

@app.route("/", methods=['POST', 'GET'])
def index():

    titles = Blog.query.all()
    authors = Blog.query.all()
    dates = Blog.query.all()
    contents = Blog.query.all()

    return render_template("blog.html", title="Build A Blog", 
        titles=titles, contents=contents,
        authors=authors, dates=dates)

@app.route("/newpost", methods=['POST', 'GET'])
def submit_post():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        date = request.form['date']
        content = request.form['content']
        
        blog_post = Blog(title, author, date, content)
        db.session.add(blog_post)
        db.session.commit()
        return redirect ('/')

    return render_template("newpost.html")

@app.route("/display")
def display_form():
    return render_template("display.html")

if __name__ == '__main__':
    app.run()