"""
Hanwei Wang
Time: 13-2-2020 10:19
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
    # 中文的话是需要特别注意的地方以及需要检查的地方
"""

from flask import Blueprint, render_template, flash, request
from flask_login import current_user
from Webapp.models import Post, Category, User
from Webapp.extensions import db

post_bp = Blueprint('post', __name__)

@post_bp.route("/<post_id>") # post_id 在这个route函数被调用时传入
def post(post_id):
    post = Post.query.get_or_404(post_id)
    picture_list = post.picture_list
    picture_list = picture_list.split('\\')
    # get posts with similar category, and show 5 of them
    category = post.categories
    # category = Category.query.get(post.categories)
    like_posts = category[0].posts[0:5]

    if post.classification =='vip1':
        if current_user.is_authenticated:
            if current_user.vip1 == 'yes':
                return render_template('post_content.html', title=post.title, post=post, picture_list=picture_list[:-1],
                                       like_posts=like_posts)
            else:
                return render_template('404_not_allowed_to_visit.html')
        else:
            return render_template('404_not_allowed_to_visit.html')

    elif post.classification == 'vip2':
        if current_user.is_authenticated:
            if current_user.vip2 == 'yes':
                return render_template('post_content.html', title=post.title, post=post, picture_list=picture_list[:-1],
                                       like_posts=like_posts)
            else:
                return render_template('404_not_allowed_to_visit.html')
        else:
            return render_template('404_not_allowed_to_visit.html')

    else:
        return render_template('post_content.html', title=post.title, post=post, picture_list = picture_list[:-1], like_posts = like_posts)


@post_bp.route('/<post_id>/add_favourite', methods = ['POST'])
def add_favourite_post_page(post_id):
    post_title = request.get_json()['post_title']
    post = Post.query.filter_by(title = post_title).first()

    if current_user.is_authenticated:
        if post in current_user.like:
            user = User.query.filter_by(id=current_user.id).first()
            user.like.remove(post)
            print(len(post.likeby))
            db.session.commit()
            post.total_like = len(post.likeby)
            db.session.commit()
            print(len(post.likeby))
        else:
            user = User.query.filter_by(id=current_user.id).first()
            user.like.append(post)
            print(len(post.likeby))
            db.session.commit()
            post.total_like = len(post.likeby)
            db.session.commit()
            print(len(post.likeby))

        post = Post.query.filter_by(title=post_title).first()
        return render_template('post_page_content_section.html', post = post,)
    else:
        flash('You have not login yet, please login or register','success')
        return render_template('post_page_content_section.html', post = post,)


