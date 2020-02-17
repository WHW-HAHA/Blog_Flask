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
    admin.set_password('Whw844409040')
    db.session.add(admin)
    db.session.commit()

def fake_posts():
