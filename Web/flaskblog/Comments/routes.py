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
from flaskblog.NewModels import Comment, Post
from flask_login import current_user
from flaskblog import db
from flaskblog.posts.routes import posts
from flask_restful import request


comments = Blueprint('comments',__name__)


# if I still need a special template for this?
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def new_comment(post_id):
    # post id is needed, as the comment points to the post
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        # No date needed, as the moment now will be used
        if current_user.is_active:
            post = Comment(content = form.content.data, author = current_user._get_current_object(), belongsto = post)
        else:
            post = Comment(content = form.content.data, auther = 'AnonymousUser', belongsto = post)
        db.session.add(post)
        db.session.commit()
        flash('Your new comment has been created!', 'success')
        # 返回当前的url, 并且更新评论
        return redirect(url_for('post.post', commentform = form,  ),)


