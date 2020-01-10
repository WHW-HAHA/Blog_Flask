"""
Hanwei Wang
Time: 10-1-2020 13:23
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
"""

from flaskblog import db
from flaskblog.models import Post, Showcase, User
from flask import flash

'''
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
'''


'''
    by_user = db.Column(db.String(20), db.ForeignKey('user.id'), primary_key = True,  nullable = False) # currently fake type, grouped by user_id
    image_file = db.Column(db.String(20), db.ForeignKey('user.image_file'), nullable = False) # link to the user profile
    amount = db.Column(db.Integer, nullable = False, default = 0)
    post = db.Column(db.Integer)
'''
# Update the content in Showcase model
def updateshowcase():
    all_post = Post.query.all()
    for post in all_post:
        by_user = post.user_id
        showcase = Showcase(by_user = by_user,
                            post = post.id)
        db.session.add(showcase)
        db.session.commit()
        flash('The content has been updated!')



