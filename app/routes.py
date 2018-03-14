from app import app
from flask import render_template, url_for, redirect

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
