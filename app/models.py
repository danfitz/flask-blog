from app import db

from datetime import datetime

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __repr__(self):
        return "<User {}>".format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    published = db.Column(db.Boolean())
    title = db.Column(db.String(100))
    slug = db.Column(db.String(50), unique=True)
    featured_img = db.Column(db.String(200))
    category = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    excerpt = db.Column(db.String(50))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("author.id"))

    def __repr__(self):
        return "<Post {}>".format(self.title)
