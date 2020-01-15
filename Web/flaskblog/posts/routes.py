from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.NewModels import Post, Comment
from flaskblog.posts.forms import PostForm
from flakblog.comments.forms import CommentForm

posts = Blueprint('posts', __name__)

# redirect() will change the route of the original url, url + route
# render_template won't change the url


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    # first to get the post
    post = Post.query.get_or_404(post_id)
    if post:
        comment_list = get_comments(post_id)
        return render_template('main.post', title=post.title, post=post, comment_list = comment_list)
    else:
        abort(403)


def get_comments(post_id):
    post = Post.query.get_or_404(post_id)
    comment_list = post.comment
    return comment_list


def make_comments(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_anonymous:
            comment = Comment(content = form.content.data, post_id = post_id)
        else:
            comment = Comment(content = form.content.data, post_id = post_id, user_id = current_user.id)
        db.session.add(comment)
        db.session.commit()
    flash('Your comment has been accepted successfully!')


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
