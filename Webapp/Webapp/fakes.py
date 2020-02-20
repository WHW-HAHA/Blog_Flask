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

# 建立1侧的模型，虚拟数据可以之后从多侧生成

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

def fake_user(count = 50):
    for i in range(count):
        user = User(username = fake.name(),
                    email = fake.email(),
                    password = 'Whw8409040',)
        db.session.add(user)
    db.session.commit()

"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # Relationship enable to visit deals by user.deal, with including back_ref, enable to call fetch the user by their deal.by
    deals = db.relationship('Deal', backref = 'by', lazy = 'dynamic')
"""


def fake_category():
    categeory_list = ["Categeory 1", "Categeory 2", "Categeory 3", "Categeory 4",]
    for Name in categeory_list:
        categeory = Category( name = Name )
        db.session.add(categeory)
    db.session.commit()


def fake_post(count = 50):
    for i in range(count):
        post = Post( title = fake.sentence(),
                     content = fake.text(500),
                     date_posted = fake.date_of_birth(),
                     price = fake.random_int(0, 100),
                     )
        # still missing the category
        for j in range(random.randint(1,5)):
            categeory = Category.query.get(random.randint(1, Category.query.count()))
            if categeory not in post.categories:
                post.categories.append(categeory)
        db.session.add(post)
    db.session.commit()


def fake_deal(count = 10):
    for i in range(count):
        deal = Deal( time = fake.birthday(),
                     by_id = User.query().get(random.randint(1, User.query().count())),
                     posts = Post.query().get(random.randint(1, Post.query().count())))
        db.sesion.add(deal)
    db.session.commit()
