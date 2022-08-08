from crypt import methods
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, DEFAULT_USER_IMG, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "programare"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

#############  HOME ROUTE  ###############

@app.route('/')
def home():
    """Shows most recent 5 posts"""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('posts/home.html', posts=posts)


##############  404 ROUTE  ################

@app.errorhandler(404)
def page_not_found(e):
    """Shows CUSTOM page not found """
    return render_template('404.html')


############### USER ROUTES  ###############

@app.route('/users')
def users_listing():
    """Lists all users alphabetically"""
    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template('users/index.html', users=users)


@app.route('/users/new')
def add_user():
    """Form for adding new user"""
    return render_template('users/new.html')


@app.route('/users/new', methods=['POST'])
def user_process():
    """Form submitting data to db"""
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    # WHY IS THIS NOT WORKING?? image_url not diplayed. Why is not taking the global vairable?
    # image_url = request.form.get("image_url", DEFAULT_USER_IMG)   
    image_url = request.form['image_url'] or None
    user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} added.")

    return redirect("/users")


@app.route('/users/<int:id>')
def show_user(id):
    """Shows user's details with Edit and Delete buttons"""
    user = User.query.get_or_404(id)
    return render_template("users/show.html", user=user)


@app.route('/users/<int:id>/edit')
def edit_user(id):
    """Shows a form for editing user data"""
    user = User.query.get_or_404(id)
    return render_template("users/edit.html", user=user)


@app.route("/users/<int:id>/edit", methods=['POST'])
def save_user(id):
    """Saving edited data in db"""
    user = User.query.get_or_404(id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash("Changes saved")
    return redirect("/users")

@app.route("/users/<int:id>/delete", methods=['POST'])
def delete_user(id):
    """Deleting user from db"""
    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted")
    return redirect('/users')


############### POSTing ROUTES ###############

@app.route("/users/<int:id>/posts/new")
def post_form(id):
    """Shows form for adding a post - based on user id"""

    user = User.query.get_or_404(id)
    return render_template("posts/new.html", user=user)


@app.route("/users/<int:id>/posts/new", methods=["POST"])
def post_submit(id):
    """Submitting form for a new post"""

    user = User.query.get_or_404(id)
    title = request.form['title']
    content = request.form['content']
    post = Post(title=title, content=content, user_id=user.id)

    db.session.add(post)
    db.session.commit()
    flash("New Post Added")
    return redirect(f"/users/{user.id}")


@app.route("/posts/<int:id>")
def show_post(id):
    """Shows a post based on post id"""

    post = Post.query.get_or_404(id)
    return render_template('posts/show.html', post=post)


@app.route("/posts/<int:id>/edit")
def edit_post(id):
    """Shows form for editing the post"""

    post = Post.query.get_or_404(id)
    return render_template('posts/edit.html', post=post)


@app.route("/posts/<int:id>/edit", methods=["POST"])
def update_post(id):
    """Form submition for updating the post"""

    post = Post.query.get_or_404(id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash("Post updated")
    return redirect(f"/users/{post.user_id}")


@app.route("/posts/<int:id>/delete", methods=['POST'])
def delete_post(id):
    """Handles deleting post"""

    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash("Post gone forever and ever")
    return redirect(f"/users/{post.user_id}")
