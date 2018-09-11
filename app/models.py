#!/usr/bin/env python
from . import app

import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from slugify import slugify

database_file = "sqlite:///database.db"

db = SQLAlchemy(app)

#reference
#https://overiq.com/flask/0.12/database-modelling-in-flask/

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    body  = db.Column(db.String,unique=True, nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)    
    
    #one to many relationship
    #parent category, child post

    #category_id attribute of the Post model can only take values 
    #from the id column of the categories table.
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))


    #def __repr__(self):
    #    return "<Title: {}>".format(self.title)
    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title)

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    #one to many relationship
    #parent category, child post

    #The posts attributes only exist for your convenience they are not actual columns in the table.
    posts = db.relationship('Post', backref='category')

    def __repr__(self):
        return "<{}: {}>".format(self.id, self.name)

#A blog post is usually associated with one or more tags. 
#Similarly, a tag is also associated with one or more posts. 
#So there is a many-to-many relationship between posts and tags.
#Create a new table called association table by defining 2 foreign keys 
#referencing post.id and tag.id columns.
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    #many to many relationship
    posts = db.relationship('Post', secondary=post_tags, backref='tags')

    def __repr__(self):
        return "<{}:{}>".format(id, self.name)



#utility functions to be used by flask shell in command line

#generate the slug field for all posts, based on post title
def generate_slugs():
    posts = db.session.query(Post)
    for post in posts:
        post.slug = slugify(post.title)
    db.session.commit()
