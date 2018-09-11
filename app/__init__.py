#!/usr/bin/env python
import os
from datetime import datetime

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from wtforms import Form, StringField, SelectField, validators
from flask_table import Table, Col, LinkCol


#create the web app
app = Flask(__name__)

#connect to the melodyyu.com database
app.config["SQLALCHEMY_DATABASE_URI"] =  "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)
from .models import db
from .models import Tag, Post, Category


@app.route('/posts')
def posts():
    results = []
    posts_qry = db.session.query(Post)
    category_qry = db.session.query(Category)
    articles = posts_qry.all()
    categories = category_qry.all()
    #print(results)

    if not articles:
        flash('No posts found!')
        return redirect('/')
    else:
        # display results
        return render_template('posts.html', posts = articles, categories = categories)

@app.route('/', methods=["GET", "POST"])
def home():
    return redirect('/posts')

@app.route("/view", methods=["GET","POST"])
def view():
    post_id = request.args.get("id")
    #print(post_id)
    if request.method == 'POST':
        #print(request.form)
        post_id = request.form.get("id")
    else:
        post_id = request.args.get("id")
    try:
        #post = db.session.query(Post).filter(Post.id == post_id).first()
        post = Post.query.filter_by(id = post_id).first()
        db.session.add(post)
        db.session.commit()
    except Exception as e:
            print("Failed to query a post to SQL database")
            #print(e)
            return page_not_found(e)
    return render_template("view.html", post = post)


@app.route("/recent")
def recent():
    results = []
    posts_qry = db.session.query(Post)
    articles = posts_qry.all()

    if not articles:
        flash('No posts found!')
        return redirect('/')
    else:
        # display results
        return render_template('recent.html', posts = articles)


@app.route("/page/<slug>")
def view_post(slug):
    """View a post by slug"""
    post = Post.query.filter_by(slug=slug).first()
    if not post:
        return redirect('/')
    return render_template("view.html", post = post)


@app.route("/category/<category>")
def view_category(category):
    try:
        c_qry = Category.query.filter_by(name = category).first()
        if not c_qry:
            return redirect('/')
        else:
            posts = Post.query.filter_by(category_id = c_qry.id).all()
            print(posts)
    except Exception as e:
            print("Failed to query a post to SQL database")
            #print(e)
            return page_not_found(e)
    return render_template("category.html", posts = posts, category = category.capitalize())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/people')
def people():
    return render_template('people.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
