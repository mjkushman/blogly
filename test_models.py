from unittest import TestCase

from app import app
from models import db, User, Post


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_ECHO"] = False
app.config["SECRET_KEY"] = "mysecurepassword"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


db.drop_all()
db.create_all()

class UserModelsTestCase(TestCase):
    """Tests models for Blogly app"""
    def setUp(self):
        User.query.delete() #delete any existing rows

    def tearDown(self):
        db.session.rollback() #clear out the sesion
    
    def test_create_post(self):
        post = Post(title='My Test Post',content='Here is a string of content')

        self.assertEqual(post.title,'My Test Post')
        self.assertEqual(post.content,'Here is a string of content')

        db.session.add(post)
        db.session.commit()
        self.assertTrue(post.id) #Check for id, only available after commit
   
    def test_create_user(self):
        user = User(first_name='Mike',last_name='Kushman',image_url='https://images.pexels.com/photos/1057222/pexels-photo-1057222.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1')

        self.assertEqual(user.first_name,'Mike')
        self.assertEqual(user.last_name,'Kushman')
        db.session.add(user)
        db.session.commit()
        
        self.assertTrue(user.id) #Check for id, only available after commit


    def test_post_user_relation(self):
        user = User(first_name='Peter',last_name='Pan',image_url='https://images.pexels.com/photos/1057222/pexels-photo-1057222.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1')
        db.session.add(user)
        db.session.commit()
        
        post = Post(title='My Test Post',content='Here is a string of content',user_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.assertEqual(user.id,post.user_id) #make sure id's match up
        self.assertTrue(len(user.posts)>0) # make sure a post is returned

\