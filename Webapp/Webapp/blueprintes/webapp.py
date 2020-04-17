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

from flask import Blueprint, request, render_template, flash, redirect, url_for
from Webapp.models import Post, User, Category
from sqlalchemy import and_, or_
from flask_login import current_user
from Webapp.extensions import db
from datetime import datetime, timedelta

webapp_bp = Blueprint('webapp', __name__)

@webapp_bp.route('/')
@webapp_bp.route('/welcome')
def welcome():
    category2 = Category.query.get(2)
    category3 = Category.query.get(3)
    category4 = Category.query.get(4)
    post_list_1 = Post.query.order_by(Post.date_posted.desc()).all()[0:5]
    post_list_2 = category2.posts[0:5]
    post_list_3 = category3.posts[0:5]
    post_list_4 = category4.posts[0:5]
    return render_template('welcome.html',category_asia= category2, category_usa= category3, category_cartoon= category4,
                           list1 = post_list_1, list2 = post_list_2, list3 = post_list_3, list4 = post_list_4)

@webapp_bp.route('/gotocategory/<name>')
def go_to_category(name):
    if name == 'TheLatest':
        name = 'The latest'
    if name == 'Europe&USA':
        name = 'Europe & USA'
    category_name = name
    category = Category.query.filter_by(name = category_name).first()
    posts = category.posts
    return render_template('category_content.html', category = category, posts = posts )

def take_total_like(elem):
    return elem.total_like

def take_time_posted(elem):
    return elem.date_posted

def bubbleSort_by_totallike(nums):
    for i in range(len(nums) - 1):
        for j in range(len(nums) - i - 1):
            if nums[j].total_like < nums[j+1].total_like:
                nums[j], nums[j+1] = nums[j+1], nums[j]
    return nums

def bubbleSort_by_time(nums):
    for i in range(len(nums) - 1):
        for j in range(len(nums) - i - 1):
            if nums[j].date_posted < nums[j+1].date_posted:
                nums[j], nums[j+1] = nums[j+1], nums[j]
    return nums

@webapp_bp.route('/gotocategory/<categoryName>/sorted', methods = ['POST'])
def sort_content_TheLatest(categoryName):
    sort_by = request.get_json()['by']
    if categoryName == 'TheLatest':
        categoryName = 'The latest'
    if categoryName == 'Europe&USA':
        categoryName = 'Europe & USA'
    if sort_by == 'popularity':
        posts_all = Category.query.filter_by(name = categoryName).first().posts
        posts = bubbleSort_by_totallike(list(posts_all))
    if sort_by == 'time':
        posts_all = Category.query.filter_by(name = categoryName).first().posts
        posts = bubbleSort_by_time(list(posts_all))

    return render_template('category_content_section.html', posts = posts, category = Category.query.filter_by(name = categoryName) )

@webapp_bp.route('/gotocategory/<categoryName>/add_favourite', methods = ['POST'])
def add_favourite_content_page(categoryName):
    post_title = request.get_json()['post_title']
    categoryName = request.get_json()['categoryName']
    post = Post.query.filter_by(title = post_title).first()
    if categoryName == 'TheLatest':
        categoryName = 'The latest'
    if categoryName == 'Europe&USA':
        categoryName = 'Europe & USA'
    category = Category.query.filter_by(name = categoryName).first()
    if current_user.is_authenticated:
        if post in current_user.like:
            current_user.like.remove(post)
            post.total_like = len(post.likeby)
            db.session.commit()

        else:
            current_user.like.append(post)
            post.total_like = len(post.likeby)
            db.session.commit()

        post = Post.query.filter_by(title=post_title).first()
        return render_template('post_content_section.html', post = post, category=category)
    else:
        flash('You haven login yet, please login or register','success')
        return render_template('post_content_section.html', post = post, category=category)

@webapp_bp.route('/search/add_favourite', methods = ['POST'])
def add_favourite_search_page():
    post_title = request.get_json()['post_title']
    post = Post.query.filter_by(title = post_title).first()
    if current_user.is_authenticated:
        if post in current_user.like:
            current_user.like.remove(post)
            post.total_like = len(post.likeby)
            db.session.commit()

        else:
            current_user.like.append(post)
            post.total_like = len(post.likeby)
            db.session.commit()

        post = Post.query.filter_by(title=post_title).first()
        return render_template('post_content_section.html', post = post)
    else:
        flash('You haven login yet, please login or register','success')
        return render_template('post_content_section.html', post = post)

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
    return render_template('test.html', title='About')


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
        ## search in user is no need
        keyword = request.form.get('keyword')
        if keyword =="":
        # print('Keyword is {}'.format(keyword))
        # user_found = User.query.filter(
        #     User.username.like('%' + keyword + '%') if keyword is not None else '',).all()
        # search in posts
            return render_template('search_nofound.html', title='no results have been found', keyword = keyword )
        else:
            page = request.args.get('page', 1, type=int)
            post_found = Post.query.filter(or_(
                Post.title.like('%' + keyword + '%') if keyword is not None else '',
                Post.subtitle.like('%' + keyword + '%') if keyword is not None else '',
                Post.content.like('%' + keyword + '%') if keyword is not None else ''))
            post = post_found.order_by(Post.date_posted.desc()).paginate(page,per_page=10)
            # highlight the keyword in result page
            if post_found.all():
                flash('We had found these for you!')
                return render_template('search_found.html', title = 'results of search', posts = post, keyword = keyword)
            else:
                return render_template('search_nofound.html', title = 'no results have been found', keyword = keyword)

@webapp_bp.route("/get_temporary_vip")
def one_day_VIP():
    if current_user.vip_try_out:
        current_user.membership_date = datetime.now()
        expire_date = current_user.membership_date + timedelta(days=1)
        current_user.vip_try_out = 0
        flash("Enjoy your exploration, your temporary VIP will expire in one day.")
        return redirect(url_for('webapp.VIP_check'))
        # here should redirect to the VIP content page
    else:
        return render_template('create_share_link.html')

@webapp_bp.route("/VIP")
def VIP_check():
    if current_user.is_authenticated:
        if current_user.membership:
            return render_template('vip_entrance.html')
        else:
            flash('You are currently not a VIP. Get your temporary VIP here!','success')
            return render_template('temporary_vip.html')
    else:
        flash("You haven't login yet, please login first", "warning")
        return redirect(url_for("user.login"))

