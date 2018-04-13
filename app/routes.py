from flask import render_template, url_for, redirect, flash, request
from app import app, db

from app.models import Author, Post
from app.forms import LoginForm, PublishForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
import os, shutil

# returns index.html showing non-journal posts in descending timestamp order
@app.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.filter(
        Post.published==True,
        Post.category!="journal").order_by(
            Post.timestamp.desc()).paginate(
                page, app.config["POSTS_PER_PAGE"], False)
    next_url = url_for("index", page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for("index", page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("index.html", title="Dan Fitz", posts=posts.items, next_url=next_url, prev_url=prev_url)

# returns journal.html showing journal posts in descending timestamp order
@app.route("/journal")
@login_required
def journal():
    page = request.args.get("page", 1, type=int)
    journal_posts = Post.query.filter(
        Post.published==True,
        Post.category=="journal").order_by(
            Post.timestamp.desc()).paginate(
                page, app.config["POSTS_PER_PAGE"], False)
    next_url = url_for("journal", page=journal_posts.next_num) \
        if journal_posts.has_next else None
    prev_url = url_for("journal", page=journal_posts.prev_num) \
        if journal_posts.has_prev else None
    return render_template("journal.html", title="Journal", posts=journal_posts.items, next_url=next_url, prev_url=prev_url)

# returns specific post according to its unique slug
@app.route("/post/<slug>")
def post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template("post.html", title=post.title, post=post)

# dashboard displaying DRAFTS and then all published posts by categories
@app.route("/dashboard")
def dashboard():
    drafts = Post.query.filter_by(published=False).order_by(Post.timestamp.desc())
    first_world_problems = Post.query.filter_by(category="first-world-problems").order_by(Post.timestamp.desc())
    self_actualization = Post.query.filter_by(category="self_actualization").order_by(Post.timestamp.desc())
    relationships = Post.query.filter_by(category="relationships").order_by(Post.timestamp.desc())
    journal = Post.query.filter_by(category="journal").order_by(Post.timestamp.desc())
    categories = zip([drafts, first_world_problems, self_actualization, relationships, journal], ["Drafts", "First World Problems", "Self-actualization", "Relationships", "Journal"])
    return render_template("dashboard.html", title="Dashboard", categories=categories)

# submits new post to database
@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    form = PublishForm()
    if form.validate_on_submit():
        # creates post instance
        post = Post(
            timestamp=datetime.utcnow(),
            published=form.published.data,
            featured_img=form.featured_img.data,
            title=form.title.data,
            slug=form.slug.data,
            category=form.category.data,
            excerpt=form.excerpt.data,
            content=form.content.data,
            author=current_user
        )

        # commits post instance to database
        db.session.add(post)
        db.session.commit()

        if post.published == True:
            flash("'{}' published!".format(post.title))
        else:
            flash("'{}' drafted!".format(post.title))
        return redirect(url_for("index"))

    return render_template("new.html", title="New Post", form=form)

# edits posts already in database
@app.route("/edit/<slug>", methods=["GET", "POST"])
@login_required
def edit(slug):
    # grabs post by slug
    post = Post.query.filter_by(slug=slug).first()
    form = PublishForm()

    # populates form with current post instance's attributes when entering editing page
    if request.method == "GET":
        form.published.data = post.published
        form.featured_img.data = post.featured_img
        form.title.data = post.title
        form.slug.data = post.slug
        form.category.data = post.category
        form.excerpt.data = post.excerpt
        form.content.data = post.content

    elif form.validate_on_submit():
        if form.update_timestamp.data == True:
            # updates timestamp to current time IF prompted by user
            post.timestamp = datetime.utcnow()
        post.published = form.published.data
        post.featured_img = form.featured_img.data
        post.title = form.title.data
        post.slug = form.slug.data
        post.category = form.category.data
        post.excerpt = form.excerpt.data
        post.content = form.content.data

        # commits post instance to database
        db.session.add(post)
        db.session.commit()

        if post.published == True:
            flash("'{}' published!".format(post.title))
        else:
            flash("'{}' drafted!".format(post.title))
        return redirect(url_for("post", slug=post.slug))

    return render_template("edit.html", title="Edit Post", form=form)

# login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        # grabs author instance from username provided in login form
        author = Author.query.filter_by(username=form.username.data).first()

        # flashes error if username or password invalid upon form submission
        if author is None or not author.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))

        # logs in user
        login_user(author, remember=form.remember_me.data)
        flash("Hi, {}!".format(author.username))

        # sends user to the page in "next" arg
        next_page = request.args.get("next")
        # if there is no "next" arg or there is a netloc in the "next" arg, sends to index
        ## note: this is used to prevent malicious redirects
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("dashboard")
        return redirect(next_page)

    return render_template("login.html", title="Log In", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
