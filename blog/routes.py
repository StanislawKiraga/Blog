from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from blog import app, db


@app.route('/')
def home():
    return render_template('base.html')