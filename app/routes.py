from flask import render_template, url_for, redirect, flash, request
from app import app

from app.models import Author
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route("/")
def index():
    posts = [
        {
            "title": "Hygge",
            "content": "Hygge can increase happiness by a few points.",
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
