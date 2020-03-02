"""
Hanwei Wang
Time: 26-2-2020 15:38
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
    # 中文的话是需要特别注意的地方以及需要检查的地方
"""
from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from Webapp.forms.user import RegistrationForm, LoginForm, UpdateAccountForm
from Webapp.models import User
from Webapp import db, bcrypt
user_bp = Blueprint('user', __name__)

# redirect 重定向url
# render_template 不改变当前的url
# form.validate_on_submit(), 会自动检查页面内的POST 和 GET 请求的表单是否符合要求

@user_bp.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('webapp.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # hash the original user password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username = form.username.data, email = form.email.data,
                    password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to login in!')
        return redirect(url_for('user.login'))
    return render_template('register.html', title = 'Register', form = form)

@user_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('webapp.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            return redirect(url_for('webapp.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# put the user information and functionality all in account page
@user_bp.route('/account', methods = ['GET', 'POST'])
def account():
    return redirect(url_for('user.account'))


@user_bp.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('webapp.home'))














