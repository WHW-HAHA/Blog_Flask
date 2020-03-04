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

from flask import Blueprint

post_bp = Blueprint('post', __name__)

@post_bp.route("/post/<int:post_id>") # post_id 在这个route函数被调用时传入
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


