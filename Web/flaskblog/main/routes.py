from flask import render_template, request, Blueprint
from flaskblog.models import Post, Showcase

# updateshowcase()
main = Blueprint('main', __name__)

@main.route("/")
def welcome():
    return render_template('index.html')

@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    List = [1, 2, 3]
    showcase = Showcase.query.all()
    return render_template('home_showcase.html', posts=posts, showcase = showcase)

@main.route("/about")
def about():
    return render_template('about.html', title='About')
