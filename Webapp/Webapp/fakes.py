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

import random
from faker import Faker

from Webapp import db
from Webapp.models import Admin, Category, Post, Deal, User

fake = Faker()

def fake_admin():
    admin = Admin(
        username = 'admin',
        post_title = 'TheFirstPost',
        post_sub_title = 'SubtitleOfTheFirstPost',
    )
    admin.set_password('NotAPassword')
    db.session.add(admin)
    db.session.commit()

def fake_category():
    categeory_list = ["Categeory 1", "Categeory 2", "Categeory 3", "Categeory 4",]
    for Name in categeory_list:
        categeory = Category( name = Name )

        db.session.add(categeory)
        db.session.commit()

def fake_posts(count = 50):
    categeory_list = ["Categeory 1", "Categeory 2", "Categeory 3", "Categeory 4",]
    for i in range(count):
        post = Post( title = fake.sentence(),
                     content = fake.text(500),
                     date_posted = fake.date_of_birth(),
                     price = fake.random_int(0, 100),
                     # still missing the category
                     category = random.choice(categeory_list)
                     )
        db.session.add(post)
        db.session.commit()


"""

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), unique = True)
    # posts = db.relationship('Post', back_populates = 'category')


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable = False, default = 0)
    category = db.relationship("Category", secondary= post_category_collections, backref = "post", lazy = 'dynamic')
"""
