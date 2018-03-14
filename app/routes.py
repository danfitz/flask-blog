from flask import render_template, url_for, redirect, flash
from app import app
from app.forms import LoginForm

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
    form = LoginForm()
    if form.validate_on_submit():
        flash("Hi, Dan!")
        return redirect(url_for("index"))
    return render_template("login.html", title="Log In", form=form)
