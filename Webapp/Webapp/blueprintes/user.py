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
from flask import Blueprint, render_template, redirect, flash, url_for, session, jsonify, request
from flask_login import current_user, login_user, logout_user, login_required
from Webapp.forms.user import RegistrationForm, LoginForm, UpdateProfileForm, UpdatePasswordForm, UpdateProfilePicForm, RequestResetForm, ResetPasswordForm
from Webapp.models import User, Deal, Post, Category
from Webapp import db, bcrypt, mail
from flask_mail import Message
import os
import secrets
from PIL import Image
from flask import current_app
import re
import time
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from weixin.login import WeixinLogin
from collections import Counter
import random

user_bp = Blueprint('user', __name__)

app_id = ''
app_secret = ''
wx_login = WeixinLogin(app_id, app_secret)


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


@user_bp.route('/get_share_code', methods=['POST'])
def get_share_link():
    if current_user.is_authenticated:
        if current_user.invitation_code:
            invitation_code = current_user.invitation_code
            flash('You already have a invitation code, you can check your unique invitation code in your account.', 'success')
            return render_template('post_content_section.html', invitation_code = invitation_code)
        else:
            invitation_code = generate_verification_code()
            current_user.invitation_code = invitation_code
            db.session.commit()
            flash('Here is your invitation code, you can check your unique invitation code in your account.', 'success')
            return render_template('post_content_section.html', )
    else:
        flash("You haven't login yet, please login first!", 'warning')
        return redirect('user.login')

def generate_verification_code():
    code_list = []
    for i in range(10): # 0-9数字
        code_list.append(str(i))
    for i in range(65, 91): # A-Z
        code_list.append(chr(i))
    for i in range(97, 123): # a-z
        code_list.append(chr(i))

    myslice = random.sample(code_list, 12)  # 从list中随机获取12个元素，作为一个片断返回
    share_code = ''.join(myslice) # list to string
    return share_code


@user_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('webapp.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first() # remember to get the first item
        # here not able to check the hashed user password yet if user and bcrypt.check_password_hash(user.password, form.password.data):
        if user and user.password == form.password.data:
            login_user(user, remember = form.remember.data)
            return redirect(url_for('webapp.welcome'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

def xml_parser(text):
    dic = {}
    soup = BeautifulSoup(text, 'html.parser')
    div = soup.find(name='error')
    for item in div.find_all(recursive=False):
        dic[item.name] = item.text
    return dic

# put the user information and functionality all in account page
@user_bp.route('/account')
@login_required
def account():
    user = current_user
    if user.membership == 'none':
        membership_message = "You are not a member!"
    if user.membership == 'week':
        membership_expire = user.membership_date + timedelta(weeks = 1) - datetime.now()
        # membership_expire = membership_expire.strftime("%Y-%m-%d")
        membership_message = 'Expire in {}'.format(membership_expire)
    if user.membership == 'month':
        membership_expire = user.membership_date + timedelta(weeks = 4) - datetime.now()
        # membership_expire = membership_expire.strftime("%Y-%m-%d")
        membership_message = 'Expire in {}'.format(membership_expire)
    if user.membership == 'year':
        membership_expire = user.membership_date + timedelta(weeks = 52) - datetime.now()
        # membership_expire = membership_expire.strftime("%Y-%m-%d")
        membership_message = 'Expire in {}'.format(membership_expire)

    likes_all = user.like # return a query
    deals_all = user.deals
    # deals_all = Deal.query.filter_by(by_id = user.id).order_by(Deal.time.desc()).all() # query.*.all() return a list
    item_id = []
    for deal in deals_all:
        item_id.append(deal.item_id)
        deal.price = Post.query.get(deal.item_id).price
        deal.title = Post.query.get(deal.item_id).title
        deal.image_file = Post.query.get(deal.item_id).image_file
    total_buys = len(deals_all)
    total_likes = len(likes_all)

    return render_template('account.html', message = '', title = user.username, user = user, deals = likes_all, total_buys= total_buys,
                           total_likes = total_likes, membership_message = membership_message)

@user_bp.route('/account/update', methods = ['POST'])
@login_required
def account_update():
    category = request.get_json()['category']
    if category == 'likes':
        if current_user.like:
            posts = current_user.like
            message = ''
        else:
            posts = []
            message = "You haven't like anything"

    if category == 'buys':
        # get all the posts have been brought by this user
        if current_user.deals:
            posts = []
            for deal in current_user.deals:
                brought_post = Post.query.get(deal.item_id)
                posts.append(brought_post)
            message = ''
        else:
            posts = []
            message = "You haven't brought anything"


    if category == 'similar':
        # get the category this user may like
        categories = []
        if current_user.like:
            for post in current_user.like:
                for category in post.categories:
                    categories.append(category)
            top_2_likes = Counter(categories).most_common(2)
            if len(top_2_likes) == 2:
                similar_post_1 = top_2_likes[0][0].posts
                similar_post_2 = top_2_likes[1][0].posts
                similar_post = similar_post_1 + similar_post_2
            if len(top_2_likes) ==1:
                similar_post = top_2_likes[0][0].posts
            if current_user.deals:
                for deal in current_user.deals:
                    brought_post = Post.query.get(deal.item_id)
                    try:
                        similar_post.pop(brought_post)
                    except:
                        pass
                posts = similar_post
                message = ''
        else:
            posts = Post.query.order_by(Post.date_posted.desc()).all()[:10]
            message = ''

    return render_template('content_section.html', posts = posts, message = message, category = Category.query.get(1))


@user_bp.route('/user/edit_profile', methods = ['GET', 'POST'])
@login_required # the account page only accessible when ...
def update_profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.new_email.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('user.account'))
    return render_template('edit_profile.html', form = form)

@user_bp.route('/user/change_password', methods = ['GET', 'POST'])
@login_required # the account page only accessible when ...
def change_password():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        if current_user.password == form.old_password.data:
            current_user.password = form.new_password.data
            db.session.commit()
            flash('Your password has been changed!', 'success')
            return redirect(url_for('user.account'))
        else:
            flash("The old password doesn't match your current password, please check!.", 'danger')
            return render_template('change_password.html', form = form)
    return render_template('change_password.html', form = form)

@user_bp.route('/user/change_profile_pic', methods = ['GET', 'POST'])
@login_required
def change_profile_pic():
    form = UpdateProfilePicForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            db.session.commit()
            flash('Your profile picture has been changed!', 'success')
            return redirect(url_for('user.account'))
    return render_template('change_profile_pic.html', form = form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # if user frofile folder doesn't exist, create first
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='hhhh@hhhh.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
                    {url_for('user.reset_token', token=token, _external=True)}
                    If you did not make this request then simply ignore this email and no changes will be made.
                '''
    mail.send(msg)

@user_bp.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('webapp.welcome'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('user.login'))
    return render_template('reset_request.html', title = 'Reset Password', form = form)

@user_bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('user.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # user.password = hashed_password
        user.password = form.password.data
        db.session.commit()
        flash('Your password has been updated! You are now able to log in.', 'success')
        return redirect(url_for('user.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@user_bp.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    flash('You have logged out!', 'success')
    return redirect(url_for('webapp.welcome'))

@user_bp.route('/weixin-login')
def weixin_login():
    """登陆跳转地址"""
    openid = request.cookies.get("openid")
    next = request.args.get("next") or request.referrer or "/",
    if openid:
        return redirect(next)

    callback = url_for("user.authorized", next=next, _external=True)
    url = wx_login.authorize(callback, "snsapi_base")
    return redirect(url)

@user_bp.route("/authorized")
def authorized():

    code = request.args.get("code")
    if not code:
        return "ERR_INVALID_CODE", 400
    next = request.args.get("next", "/")
    data = wx_login.access_token(code)
    openid = data.openid
    resp = redirect(next)
    expires = datetime.now() + timedelta(days=1)
    resp.set_cookie("openid", openid, expires=expires)
    return resp

@user_bp.route('check/weixin-login')
def check_login():
    """
    发送GET请求检测是否已经扫码、登录
    https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid=QbeUOBatKw==&tip=0&r=-1036255891&_=1525749595604
    :return:
    """
    response = {'code': 408}
    qcode = session.get('qcode')
    ctime = str(int(time.time() * 1000))
    check_url = "https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}&tip=0&r=-1036255891&_={1}".format(
        qcode, ctime)
    ret = requests.get(check_url)
    print("ret.text~~~~~~~", ret.text)
    if "code=201" in ret.text:
        # 扫码成功
        src = re.findall("userAvatar = '(.*)';", ret.text)[0]
        response['code'] = 201
        response['src'] = src
    elif 'code=200' in ret.text:
        # 确认登录
        print("code=200~~~~~~~", ret.text)
        redirect_uri = re.findall('redirect_uri="(.*)";', ret.text)[0]
        # 向redirect_uri地址发送请求，获取凭证相关信息
        redirect_uri = redirect_uri + "&fun=new&version=v2"
        ticket_ret = requests.get(redirect_uri)
        ticket_dict = xml_parser(ticket_ret.text)
        session['ticket_dict'] = ticket_dict
        response['code'] = 200
    return jsonify(response)

@user_bp.route('/weixin_account')
def index():
    """
    用户数据的初始化
    https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-1039465096&lang=zh_CN&pass_ticket=q9TOX4RI4VmNiHXW9dUUl1oMzoQK2X2f3H3kn0VYm5YGNwUMO2THYMznv8DSXqp0
    :return:
    """
    ticket_dict = session.get('ticket_dict')
    init_url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-1039465096&lang=zh_CN&pass_ticket={0}".format(
        ticket_dict.get('pass_ticket'))

    data_dict = {
        "BaseRequest": {
            "DeviceID": "e750865687999321",
            "Sid": ticket_dict.get('wxsid'),
            "Uin": ticket_dict.get('wxuin'),
            "Skey": ticket_dict.get('skey'),
        }
    }
    init_ret = requests.post(
        url=init_url,
        json=data_dict
    )
    init_ret.encoding = 'utf-8'
    user_dict = init_ret.json()
    print(user_dict)
    # for user in user_dict['ContactList']:
    #     print(user.get('NickName'))

    return render_template('weixin_account.html', user_dict=user_dict)

@user_bp.route('/price')
def pay():
    return render_template('price.html')















