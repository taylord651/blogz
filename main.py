from flask import Flask, request, redirect, render_template, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(500))
    date = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, date, content, owner):
        self.title = title
        self.date = date
        self.content = content   
        self.owner = owner     

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogz = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect("/login")

@app.route("/", methods=['POST', 'GET'])
def index():
    
    #single_user_blog_post = Blog.query.filter_by(owner_id=session['owner_id']).all()

    single_user_blog_post = Blog.query.filter_by(owner_id=User.query.get("username")).all()

    user_id = request.args.get("user")

    if user_id == None:
        owner = User.query.all()
        return render_template("index.html", owner=owner)
    else: 
        user_posts = Blog.query.filter_by(owner_id=user_id).all()
        return render_template("singleuser.html", 
            user_posts=user_posts, user_id=user_id)
    
#How to display the posts of a single user?

@app.route("/blog", methods=['POST', 'GET'])
def blog():

    blog_id = request.args.get("id")
    user_id = request.args.get("user")

    if blog_id == None and user_id == None:
        blog_post = Blog.query.all()
        return render_template("blog.html", title="Blogz", 
            blog_post=blog_post)
    elif blog_id != None and user_id == None:
        blog_post = Blog.query.get(blog_id)
        return render_template("display.html", 
            blog_post=blog_post)
    elif blog_id == None and user_id != None:
        user_posts = Blog.query.filter_by(owner_id=user_id).all()
        return render_template("singleuser.html", 
            user_posts=user_posts, user_id=user_id)
    else:
        blog_post = Blog.query.all()
        return render_template("blog.html", title="Blogz", 
            blog_post=blog_post, user_id=user_id)


@app.route("/login", methods=['POST', 'GET'])
def login():

    post_id = request.args.get("id")
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']

        username_error = ""
        password_error = ""
        verify_password_error = ""

        if len(username) < 3:
            username_error = "Username required and must be at least 3 characters"

        if len(password) < 3:
            password_error = "Password required and must be at least 3 characters"

        if len(verify_password) == 0:
            verify_password_error = "Please verify your password"

        if password != verify_password:
            verify_password_error = "Password and verify_password do not match"

        if not username_error and not password_error and not verify_password_error:
            login = User(username, password)

            user = User.query.filter_by(username=username).first()

            if not user:
                flash('User does not exist. Please create an account', 'error')
                return render_template('login.html') 
            
            if user and user.password == password:
                session['username'] = username
                flash("Logged in!", "success")
                return redirect("/newpost")
            else:
                flash('User password incorrect', 'error')
                return render_template('login.html', username=username)

        else: 
            flash("Username, password and verify password required. Password and verify password must match.", "error")
            return render_template("login.html",
                username_error=username_error, password_error=password_error, 
                verify_password_error=verify_password_error,
                username=username)

    return render_template("login.html")

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    
    post_id = request.args.get("id")
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']

        username_error = ""
        password_error = ""
        verify_password_error = ""

        if len(username) < 3:
            username_error = "Username required and must be at least 3 characters"

        if len(password) < 3:
            password_error = "Password required and must be at least 3 characters"

        if len(verify_password) == 0:
            verify_password_error = "Please verify your password"

        if password != verify_password:
            verify_password_error = "Password and verify_password do not match"

        if not username_error and not password_error and not verify_password_error:

            existing_user = User.query.filter_by(username=username).first()
        
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                flash("Successfully created an account!", "success")
                return redirect ("/newpost")
            else:
                flash("Duplicate user! Please login", "error")
                return render_template("login.html", username=username)

        else: 
            flash("Username, password and verify password required. Password and verify  password must match.", "error")
            return render_template("signup.html",
                username_error=username_error, password_error=password_error, 
                verify_password_error=verify_password_error,
                username=username)

    return render_template ("signup.html")

@app.route("/logout")
def logout():
    del session['username']
    flash("Logged out", "success")
    blog_post = Blog.query.all()
    return render_template("blog.html", blog_post=blog_post)

@app.route("/newpost", methods=['POST', 'GET'])
def newpost():

    post_id = request.args.get("id")
    
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        content = request.form['content']
        owner = User.query.filter_by(username=session['username']).first()

        title_error = ""
        content_error = ""

        if len(title) == 0:
            title_error = "Title required"

        if len(content) == 0:
            content_error = "Blog content required"

        if not title_error and not content_error:
            blog_post = Blog(title, date, content, owner)
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
def display():
    return render_template("display.html")

if __name__ == '__main__':
    app.run()