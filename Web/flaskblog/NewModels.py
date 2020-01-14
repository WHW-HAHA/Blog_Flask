"""
Hanwei Wang
Time: 14-1-2020 9:50
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
"""

from flaskblog import db
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.png')
    password = db.Column(db.String(20), nullable = False)
    # Outer link
    # relationship one to many, an user can have many comments
    comment = db.relationship('Comment', backref = 'author')
    # Outer link
    # one to many, an user can have many payments
    # with backref, we can refer the user the from their payments
    paymenthistory = db.relationship('Payment', backref = 'customer')

    def get_reset_token(self, expires_sec = 600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Comment(db.model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # The comment is one to one relates to user, the input of foreignkey should be lowercase
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Adminstritor's post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    img = db.Column(db.String)
    fakecontent = db.Column(db.Text, nullable=False)
    # the documents should be stored on the domain or cloud, and then be accessed by the address
    content = db.Column(db.string, nullable = False)
    # add payments fields latter
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class PayMent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_issued = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, default = '匿名用户/Anonymous')
    price = db.Column(db.Float, nullable = False)
    # add the content of payments later

    def __repr__(self):
        return f"Payment('{self.id}', by '{self.customer_id}' on '{self.date_issued}')"











