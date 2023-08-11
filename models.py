"""Models for Blogly.
pt1: https://lessons.springboard.com/SQLAlchemy-Part-1-325f6b332e1f49cbb2c3b72f91cf73ae
pt2: 
pt3: https://lessons.springboard.com/Many-to-Many-Blogly-73a6d9ff082b4af9b83c32bc1f2515fa
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


# models below here
class User(db.Model):
    """Model for adding and editing users"""

    __tablename__ = "users"

    def __repr__(self):
        s = self
        return f"user_id: {s.id}, first_name: {s.first_name}, last_name: {s.last_name}, image_url: {s.image_url}"

    @classmethod
    def get_all_users(cls):
        return cls.query.all()

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)  # first name, required
    last_name = db.Column(db.String)  # last name, not required
    image_url = db.Column(db.String)  # profile image url



    def edit_user(
        self, first_name=first_name, last_name=last_name, image_url=image_url
    ):
        """allows editing of a user."""
        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url

    
    # def get_user_posts(self):
    #     return self.query
    # # def delete_user(self,user_id):
    # #     self.query.get(user_id).delete()


class Post(db.Model):
    __tablename__ = "posts"

    def __repr__(self):
        s = self
        return f"id: {s.id}, created_at: {s.created_at}, user: {s.user}, title: {s.title}, content: {s.content}"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content=db.Column(db.String)
    created_at=db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    user = db.relationship('User',backref='posts')

    def edit_post(self,title,content, tags):
        """updates a post"""
        self.title=title
        self.content=content
        self.tags=tags

    # tags = db.relation('Tag', secondary='posts_tags', backref='posts') #through relationship. Woops I didn't need to add it to both Post and Tag. Added to Tag only


class Tag(db.Model):
    __tablename__='tags'

    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(50), nullable=False)

    posts = db.relation('Post', secondary='posts_tags',backref='tags') #through relationship

    def edit_tag(self,name):
        """allows updating of a tag"""
        self.name=name


class PostTag(db.Model):
    __tablename__='posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
