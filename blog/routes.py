from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from blog import app, db
from blog.models import Entry

@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())

    return render_template("homepage.html", all_posts=all_posts)

