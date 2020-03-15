"""
Hanwei Wang
Time: 26-2-2020 15:49
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
    # 中文的话是需要特别注意的地方以及需要检查的地方
"""

from flask import Blueprint, request, render_template, flash
from Webapp.models import Post, User, Category
from sqlalchemy import and_, or_

webapp_bp = Blueprint('webapp', __name__)

@webapp_bp.route("/")
@webapp_bp.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    for post in Post.query.all():
        post.total_likes = len(list(post.likeby))
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    categories = Category.query.all()
    return render_template('home.html', posts=posts, categories = categories)


@webapp_bp.route("/about")
def about():
    return render_template('about.html', title='About')

@webapp_bp.route("/test")
def test():
    return render_template('new_login.html', title='Test')


@webapp_bp.route("/search", methods = ['POST'])
def search():
    if request.method == 'POST':
    # get keyword variable from form in web page
    # search in user
        keyword = request.form.get('keyword')
        print('Keyword is {}'.format(keyword))
        user_found = User.query.filter(
            User.username.like('%' + keyword + '%') if keyword is not None else '',).all()
        # search in posts
        page = request.args.get('page', 1, type=int)
        post_found = Post.query.filter(or_(
            Post.title.like('%' + keyword + '%') if keyword is not None else '',
            Post.subtitle.like('%' + keyword + '%') if keyword is not None else '',
            Post.content.like('%' + keyword + '%') if keyword is not None else ''))
        post = post_found.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

        # highlight the keyword in result page
        if user_found or post_found.all():
            return render_template('search_found.html', title = 'results of search', user = user_found, posts = post)
        else:
            return render_template('search_nofound.html', title = 'no results have been found', keyword = keyword)



