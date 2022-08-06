from email.policy import default
from flask_sqlalchemy import SQLAlchemy

DEFAULT_USER_IMG = "https://icons.iconarchive.com/icons/custom-icon-design/silky-line-user/128/user-icon.png"
db = SQLAlchemy()

def connect_db(app):
    """connecting to DB"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """App User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_USER_IMG)

    @property
    def full_name(self):
        """Returning user's full name"""
        return f"{self.first_name} {self.last_name}"
