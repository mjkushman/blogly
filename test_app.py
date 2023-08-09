"""Blogly application.
https://lessons.springboard.com/SQLAlchemy-Part-1-325f6b332e1f49cbb2c3b72f91cf73ae
"""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post
from unittest import TestCase
from flask_debugtoolbar import DebugToolbarExtension
from app import app


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "mysecurepassword"
# app.config['TESTING'] = True
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


class BloglyViewsTestCase(TestCase):
    """test the views/routes of our app"""
    
    @classmethod
    def setUp(cls):
        """Seeds the db with 7 people and 8 posts"""
        with open('seed.py') as seed:
            exec(seed.read())
        # Post.query.delete()
        # User.query.delete()
    
    def tearDown(self):
        # db.drop_all()
        db.session.rollback()

        

    def test_show_home(self): #defining a test case
        """Make sure the homepage renders"""
        with app.test_client() as client:
            response = client.get('/') #can access routes. Response comes back as JSON object
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Users</h1>',html)

    def test_show_home_list(self):
        """expecting to see a list of users"""
        with app.test_client() as client:
            # user1 = User(first_name='Michael',last_name='Kushman')
            # user2 = User(first_name='Willy',last_name='Wonka')
            # db.session.add_all([user1,user2])
            # db.session.commit()

            response = client.get('/') #can access routes. Response comes back as JSON object
            html = response.get_data(as_text=True)
            #check for Michael and Willy added to list and linked
            self.assertIn('Michael</a>',html)
            self.assertIn('William</a>',html)
            self.assertIn('<li>',html)
            self.assertEqual(response.status_code, 200)

    def test_add_user_route(self):
        with app.test_client() as client:
            data = dict(first_name='Bill',last_name='Nye',image_url='https://upload.wikimedia.org/wikipedia/commons/c/cd/Bill_Nye_2017.jpg')
            response = client.post('/users/new',data=data,follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code,200)
            self.assertIn('Bill',html) #see if Bill got added to the list


        