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

@webapp_bp.route('/')
@webapp_bp.route('/welcome')
def welcome():
    category1 = Category.query.get(1)
    category2 = Category.query.get(2)
    category3 = Category.query.get(3)
    category4 = Category.query.get(4)
    category5 = Category.query.get(5)
    category_list = Category.query.all()[1:5]
    post_list_1 = Post.query.order_by(Post.date_posted.desc()).all()[0:5]
    post_list_2 = category2.posts[0:5]
    post_list_3 = category3.posts[0:5]
    post_list_4 = category4.posts[0:5]
    post_list_5 = category5.posts[0:5]
    print(post_list_1)
    return render_template('welcome.html',category1= category1,category_list= category_list,
                           list1 = post_list_1, list2 = post_list_2, list3 = post_list_3, list4 = post_list_4, list5 = post_list_5)

@webapp_bp.route("/home")
def home():
    category_id = 0
    # this page should gives all the posts in different page
    page = request.args.get('page', 1, type=int)
    # get the page number of current page
    # if category is a valid category name
    if category_id == 0:
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    else:
        posts = Category.query.get(category_id).posts.order_by(Post.date_posted.desc()).paginate(page, per_page=5)
    for post in Post.query.all():
        post.total_likes = len(list(post.likeby))
    categories = Category.query.all()
    return render_template('home.html', posts=posts, categories = categories)

@webapp_bp.route("/about")
def about():
    return render_template('about.html', title='About')


@webapp_bp.route("/category")
def show_category():
    # Names of the categories
    # The latest, Asia, Europe & USA, Cartoon, Unclassified
    page = request.args.get('page', 1, type=int)
    posts = Category.query.filter_by(name = 'The latest').first().posts
    return render_template('category_content.html', posts = posts, category_name = 'The latest')



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



