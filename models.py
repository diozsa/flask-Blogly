from email.policy import default
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

DEFAULT_USER_IMG = "https://icons.iconarchive.com/icons/custom-icon-design/silky-line-user/128/user-icon.png"
db = SQLAlchemy()


def connect_db(app):
    """connecting to DB"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_USER_IMG)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Returning user's full name"""
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Post model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Return easy to read date."""
        return self.created_at.strftime("%c")
        # return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")




