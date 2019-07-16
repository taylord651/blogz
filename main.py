from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

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
@app.route("/blog", methods=['POST', 'GET'])
def index():

    blog_id = request.args.get("id")

    if blog_id == None:
        blog_post = Blog.query.all()
        return render_template("blog.html", title="Build A Blog", blog_post=blog_post)
    else:
        blog_post = Blog.query.get(blog_id)
        return render_template("display.html", blog_post=blog_post)

@app.route("/newpost", methods=['POST', 'GET'])
def submit_post():

    post_id = request.args.get("id")
    
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        date = request.form['date']
        content = request.form['content']

        title_error = ""
        content_error = ""

        if len(title) == 0:
            title_error = "Title required"

        if len(content) == 0:
            content_error = "Blog content required"

        if not title_error and not content_error:
            blog_post = Blog(title, author, date, content)
            db.session.add(blog_post)
            db.session.commit()

            if post_id == None:
                post_id = request.args.get("id")
                flash("Submitted a new post!", "success")
                return render_template("display.html", blog_post=blog_post)

        else: 
            flash("Title and blog content are required", "error")
            return render_template("newpost.html",
                title_error=title_error, title=title, content=content,
                content_error=content_error)

    return render_template("newpost.html")

@app.route("/display", methods=['POST', 'GET'])
def display_form():
    return render_template("display.html")
    #if request.method == 'GET':
    #blog_id = request.form['id']
    #blog = Blog.query.get(id="1")
    
        #return redirect("/blog?id={0}", blog=blog)
    
    #return "<h1>POST Request</h1>"

    #title = Blog.query.filter_by(id=session['id'].all()
    #content = Blog.query.filter_by(id=session['id'].all()
    
    #id = request.args.get('id')
    #return redirect("/display?id={0}".format(post_id), title=title)

if __name__ == '__main__':
    app.run()