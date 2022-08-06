from crypt import methods
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, DEFAULT_USER_IMG

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "programare"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home():
    """root route redirect to /users"""
    return redirect('/users')

@app.route('/users')
def users_listing():
    """Lists all users alphabetically"""
    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template('index.html', users=users)

@app.route('/users/new')
def add_user():
    """Form for adding new user"""
    return render_template('new.html')

@app.route('/users/new', methods=['POST'])
def user_process():
    """Form submitting data to db"""
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    # image_url = request.form.get("image_url", DEFAULT_USER_IMG)   Creating user without image_url. Why is this variant not taking the global vairable?
    image_url = request.form['image_url'] or None
    user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:id>')
def show_user(id):
    """Shows user's details with Edit and Delete buttons"""
    user = User.query.get_or_404(id)
    return render_template("show.html", user=user)

@app.route('/users/<int:id>/edit')
def edit_user(id):
    """Shows a form for editing user data"""
    user = User.query.get_or_404(id)
    return render_template("edit.html", user=user)

@app.route("/users/<int:id>/edit", methods=['POST'])
def save_user(id):
    """Saving edited data in db"""
    user = User.query.get_or_404(id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:id>/delete", methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')
