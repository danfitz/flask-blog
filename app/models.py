from app import app, db, login
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

class Author(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return Author.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    published = db.Column(db.Boolean)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(50), unique=True)
    category = db.Column(db.String(20))
    featured_img = db.Column(db.String(200))
    excerpt = db.Column(db.String(50))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("author.id"))

    def __repr__(self):
        return "<Post {}>".format(self.title)

    def save_img(self, img_file):
        static_folder = app.config["STATIC_FOLDER"]
        post_folder = os.path.join("posts", r"{}_{}".format(self.category, self.title))
        abs_folder = os.path.join(static_folder, post_folder)

        if not os.path.exists(abs_folder):
            os.makedirs(abs_folder)

        img_filename = self.title + img_file.filename[-4:]
        img_file.save(os.path.join(abs_folder, img_filename))

        img_path = os.path.join(post_folder, img_filename)
        return img_path

    def save_content(self):
        static_folder = app.config["STATIC_FOLDER"]
        post_folder = os.path.join("posts", r"{}_{}".format(self.category, self.title))
        abs_folder = os.path.join(static_folder, post_folder)

        if not os.path.exists(abs_folder):
            os.makedirs(abs_folder)

        post_filename = os.path.join(abs_folder, "{}.md".format(self.title))
        post_file = open(post_filename, "w")
        post_file.write(self.content)
        post_file.close()
