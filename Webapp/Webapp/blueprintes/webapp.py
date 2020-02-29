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

from flask import Blueprint, request, render_template
from Webapp.Webapp.models import Post

webapp_bp = Blueprint('webapp', __name__)

@webapp_bp.route("/")
@webapp_bp.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@webapp_bp.route("/about")
def about():
    return render_template('about.html', title='About')
