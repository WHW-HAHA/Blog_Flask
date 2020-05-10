"""
Hanwei Wang
Time: 13-2-2020 10:46
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
    # 中文的话是需要特别注意的地方以及需要检查的地方
"""
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from weixin import Weixin, WeixinError

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
bcrypt = Bcrypt()
weixin = Weixin()


@login_manager.user_loader
def load_user(user_id):
    from Webapp.Webapp.models import Admin
    super_user = Admin.query.get(int(user_id))
    print('Administrator is {}'.format(super_user))
    return super_user


login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'


