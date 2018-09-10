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

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "melodyyu_database.db"))

#create the web app
app = Flask(__name__)

#connect to the melodyyu.com database
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body  = db.Column(db.String,unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category    = db.relationship('Category', backref=db.backref(
        'posts', order_by=id),lazy=True)

    #def __repr__(self):
    #    return "<Title: {}>".format(self.title)

class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '{}' % self.name


@app.route('/posts')
def posts():
    results = []
    qry = db.session.query(Post)
    results = qry.all()
    #print(results)

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('posts.html', posts = results)

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
