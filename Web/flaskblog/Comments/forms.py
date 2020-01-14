"""
Hanwei Wang
Time: 14-1-2020 15:32
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

'''
class Comment(db.model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # The comment is one to one relates to user, the input of foreignkey should be lowercase
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
'''

'''
__init__(label=None, validators=None, filters=(), description='', 
id=None, default=None, widget=None, render_kw=None, 
_form=None, _name=None, _prefix='', _translations=None, _meta=None)
'''


class CommentForm(FlaskForm):
    # No ID included
    content = TextAreaField('Content', validators=[DataRequired(), ])
    submit = SubmitField('Post')




