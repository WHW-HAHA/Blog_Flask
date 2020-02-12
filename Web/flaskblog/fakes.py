"""
Hanwei Wang
Time: 7-2-2020 10:59
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
from sqlalchemy.exc import IntegrityError

from flaskblog import db
from flaskblog.models import Admin, User, Post, Deal, Category


fake = Faker()

def fake_admin():
    admin = Admin(
        username = 'admin',
        post_title = 'Admin Post',
        blog_sub_title = 'No, I am the real thing',
        name = 'Hanwei Wang',
        about = 'The try out'
    )
    admin.set_password('helloflask')
    db.session.add(admin)
    db.session.commit()



def fake_categories(count = 10):
    category = Category(name = 'Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name = fake.word())
        db.session.add(category)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def fake_posts(count=50):
    for i in  range(count):
        post = Post(
            title = fake.sentence(),
            content = fake.text(2000),
            category = Category.query.get(random.randint(1, Category.query.count())),
            date_posted = fake.date_time_this_year(),
            price = random.randint(1, 100)
        )
        db.session.add(post)
    db.session.commit()

