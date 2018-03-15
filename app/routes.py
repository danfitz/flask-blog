from flask import render_template, url_for, redirect, flash, request
from app import app, db

from app.models import Author, Post
from app.forms import LoginForm, NewPostForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

@app.route("/")
def index():
    posts = [
        {
            "title": "Hygge",
            "content": "*Hygge can increase happiness by a few points.* OK?",
            "url": url_for("index"),
            "featured": url_for("static", filename="images/featured/hygge.jpg")
        },
        {
            "title": "Let's write!",
            "content": "Writing is therapeutic for the soul.",
            "url": url_for("index"),
            "featured": url_for("static", filename="images/featured/paper table.jpg")
        }
    ]
    posts = Post.query.filter_by(category="first-world-problems")
    return render_template("index.html", title="Dan Fitz", posts=posts)

@app.route("/journal")
@login_required
def journal():
    journal_posts = [
        {
            "title": "Hygge",
            "excerpt": "Hygge can increase happiness by a few points.",
            "url": url_for("index"),
            "date": "November 5, 2017"
        },
        {
            "title": "Let's write!",
            "excerpt": "Writing is therapeutic for the soul.",
            "url": url_for("index"),
            "date": "October 19, 2018"
        }
    ]
    return render_template("journal.html", title="Journal", posts=journal_posts)

@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(
            timestamp=datetime.utcnow(),
            published=form.published.data,
            title=form.title.data,
            slug=form.slug.data,
            category=form.category.data,
            featured_img=form.featured_img.data,
            excerpt=form.excerpt.data,
            content=form.content.data
        )
        db.session.add(post)
        db.session.commit()
        if post.published == True:
            flash("Post {} published!".format(post.title))
        else:
            flash("Post {} drafted!".format(post.title))
        return redirect(url_for("index"))
    return render_template("new.html", title="New Post", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        author = Author.query.filter_by(username=form.username.data).first()
        if author is None or not author.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(author, remember=form.remember_me.data)
        flash("Hi, {}!".format(author.username))
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Log In", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
