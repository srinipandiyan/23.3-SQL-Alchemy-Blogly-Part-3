"""SQLA Models for Blogly app."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
default_profile_url = "https://images.unsplash.com/photo-1563089145-599997674d42?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1740&q=80"

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    first_name = db.Column(db.String(20), 
                           nullable=False)
    last_name = db.Column(db.String(20), 
                          nullable=False)
    image_url = db.Column(db.String(250), 
                          nullable=False, 
                          default=default_profile_url)
    
    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')

    def __repr__ (self):
        """Show info about user"""
        return f"<User(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', image_url='{self.image_url}')>"
    
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__ (self):
        """Show info about post"""
        return f"<Post(id={self.id}, title='{self.title}', content='{self.content}', created_at='{self.created_at}' user_id='{self.user_id}')>"
    
    @property
    def formatted_date(self):
        """Return formatted date"""
        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")
    
class PostTag(db.Model):
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    posts = db.relationship('Post', secondary="posts_tags", backref="tags")

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)
