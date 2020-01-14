"""
Hanwei Wang
Time: 14-1-2020 15:33
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
"""

from flask import  render_template, url_for, flash, redirect, Blueprint
from flaskblog.comments.forms import CommentForm
from flaskblog.NewModels import Comment
from flask_login import current_user
from flaskblog import db
from flask_restful import request


comments = Blueprint('comments',__name__)

# if I still need a special template for this?
def new_comment():
    form = CommentForm()
    if form.validate_on_submit():
        # No date needed, as the moment now will be used
        if current_user.is_active:
            post = Comment(content = form.content.data, author = current_user)
        else:
            post = Comment(content = form.content.data, auther = 'AnonymousUser')
        db.session.add(post)
        db.session.commit()
        flash('Your new comment has been created!', 'success')
        # 返回当前的url, 并且更新评论
        return render_template('', form = form, legend = 'New Comment', title = '')


