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
from blue.models import Admin, User, Post, Deal


fake = Faker()

def fake_admin():
    pass
