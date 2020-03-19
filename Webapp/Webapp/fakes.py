"""
Hanwei Wang
Time: 16-2-2020 18:31
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
    # 中文的话是需要特别注意的地方以及需要检查的地方
"""

'''
fake 数据只能从父类插入
'''
import random
from numpy import random as Random
from faker import Faker
from Webapp import db
from Webapp.models import Admin, Category, Post, Deal, User
from sqlalchemy import func

# 建立1侧的模型，虚拟数据可以之后从多侧生成

fake = Faker()


def fake_post(count = 50):
    for i in range(count):
        post = Post( title = fake.sentence(),
                     subtitle = fake.sentence(),
                     content = fake.text(500),
                     date_posted = fake.date_of_birth(),
                     price = fake.random_int(0, 100),
                     )
        db.session.add(post)

def fake_admin():
    admin = Admin(
            superusername = 'Hanwei_1',
    )
    admin.set_password('Whw844409040')
    db.session.add(admin)
    admin = Admin(
            superusername = 'Hanwei_2',
    )
    admin.set_password('Whw844409040')
    db.session.add(admin)
    db.session.commit()

def fake_user(count = 50):
    for i in range(count):
        user = User(username = fake.name(),
                    email = fake.email(),
                    password = 'Whw8409040',
                    )
        for j in range(random.randint(1, 5)):
            post = Post.query.get(random.randint(1, Post.query.count()))
            if post not in user.like:
                user.like.append(post)
    db.session.commit()


def fake_deal(count = 100):
    for i in range(count):
        deal = Deal(time = fake.date_of_birth(),
                    by = User.query.get(random.randint(1, User.query.count())),
                    what = Post.query.get(random.randint(1, Post.query.count()))
                    )
        db.session.add(deal)
    db.session.commit()

def fake_category():
    categeory_list = ["The latest", "Asia", "Europe & USA", "Cartoon", 'Unclassified']
    for Name in categeory_list:
        category = Category( name = Name,
                              description = fake.sentence(),
                              # admin = Admin.query.get(random.randint(1, 2))
                              )
        posts = Post.query.all()
        for j in Random.randint(50, size = 10):
            post = posts[j]
            category.posts.append(post)
        db.session.add(category)
    db.session.commit()

def fake_count():

    for post in Post.query.all():
        post.total_like = len(post.likeby)
        post.total_buy = len(post.deals)
    db.session.commit()











