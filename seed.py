from models import User, db, Post
from app import app

db.drop_all()
db.create_all()

#Add users
mike = User(first_name='Michael',last_name='Kushman',image_url='https://images.pexels.com/photos/1722198/pexels-photo-1722198.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1')

courtnie = User(first_name='Courtnie',last_name='Kushman',image_url='https://images.pexels.com/photos/1057222/pexels-photo-1057222.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1')

tim = User(first_name='Timothee',last_name='Chalamet',image_url='https://upload.wikimedia.org/wikipedia/commons/a/a9/Interview_with_Timoth%C3%A9e_Chalamet%2C_2019.png')

willy = User(first_name='William',last_name='Wonka',image_url='https://helios-i.mashable.com/imagery/articles/00jdsdJ5TJ5j9pExdUWjQaC/hero-image.fill.size_1248x702.v1611611940.jpg')

mamiko = User(first_name='Mamiko',last_name='Noto',image_url='https://upload.wikimedia.org/wikipedia/commons/a/a6/Mamiko_Noto_at_Otakon_20070722.jpg')

daisuke = User(first_name='Daisuke',last_name='Namikawa',image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Daisuke_Namikawa_2022-03-23.jpg/220px-Daisuke_Namikawa_2022-03-23.jpg')

miyuki = User(first_name='Miyuki',last_name='Sawashiro',image_url='https://upload.wikimedia.org/wikipedia/commons/8/88/Miyukichi%28Miyuki_Sawashiro%29.jpg')


db.session.add_all([mike,courtnie,tim,willy,mamiko,daisuke,miyuki])
db.session.commit()

# Add posts

p1 = Post(title='All the ways you wronged me',content='haha lol',user_id='1')
p2 = Post(title='My favorite poops',content='From 1 to 1000',user_id='1')
p3 = Post(title='There and back again',content='A tale as old as time',user_id='2')
p4 = Post(title='Fantastic breasts and wait what',content='Why cant you be good',user_id='2')
p5 = Post(title='Hello vodka, its me',content='I never understood you',user_id='3')
p6 = Post(title='10 Babes in Babeland',content='And other dumb things',user_id='3')
p7 = Post(title='The thing I would never do',content='finger sniffer',user_id='4')
p8 = Post(title='How to get money fast',content='Rob banks',user_id='4')

db.session.add_all([p1,p2,p3,p4,p5,p6,p7,p8])
db.session.commit()