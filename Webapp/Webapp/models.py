"""
Hanwei Wang
Time: 13-2-2020 10:20
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
    # 中文的话是需要特别注意的地方以及需要检查的地方
"""

from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from Webapp.extensions import db, login_manager
# werkzeug 路由模块
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
'''
instance

class Author(db.Model):
    __tablename__ = 'info_author'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    # 一的一方，relationship为Author 添加article属性，Author_obj.article内容是以Author_obj.id == Article.author_id的一组Article对象
    # backref（反向引用） 则为Article添加author属性，Article_obj.author内容是以Article.author_id == Author_obj.id 的Author_obj
    article = db.relationship("Article",backref='author',lazy='dynamic')
    """
    lazy: 指定sqlalchemy数据库什么时候加载数据
        select: 就是访问到属性的时候，就会全部加载该属性的数据
        joined: 对关联的两个表使用联接
        subquery: 与joined类似，但使用子子查询
        dynamic: 不加载记录，但提供加载记录的查询，也就是生成query对象
    """


class Article(db.Model):
    __tablename__ = "info_article"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20),nullable=False)
    # 多的一方，author_id 的取值范围只能在info_author.id的范围内
    author_id = db.Column(db.Integer,db.ForeignKey('info_author.id'))

'''

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Administrator class
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    post_title = db.Column(db.String(60))
    post_sub_title = db.Column(db.String(100))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # Relationship enable to visit deals by user.deal, with including back_ref, enable to call fetch the user by their deal.by
    deals = db.relationship('Deal', backref = 'by', lazy = 'dynamic')

    @staticmethod
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Deal(db.Model):
    # 1 user to multi deals
    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    # link the deal to the user who makes the deal
    by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # link the deal to the item
    item_id = db.Column(db.Integer, db.ForeignKey('post.id'))


# post 和 category 实际为多对多，应该创建关联表进行连接
post_category_collections = db.Table("post_category_collections",
                                     db.Column('post_id', db.Integer, db.ForeignKey("post.id")),
                                     db.Column('category_id', db.Integer, db.ForeignKey("category.id")))

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable = False, default = 0)
    category_id = db.relationship("Category", secondary= post_category_collections, backref = "posts", lazy = 'dynamic')
    deal = db.relationship('Deal', backref = 'item', lazy = 'dynamic')

    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # # foreignkey 是外键，连接多的一侧，此处post为多侧
    # category = db.relationship('Category', back_populates = 'posts')
    # # relationship 使得post具有category属性，
    # # back_populate 使得category类可以获得所有的所属posts, 属性名posts和Category中posts一样

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), unique = True)
    post_id = db.relationship("Post", secondary = post_category_collections, backref = 'categories', lazy = 'dynamic')

    # posts = db.relationship('Post', back_populates = 'category')



