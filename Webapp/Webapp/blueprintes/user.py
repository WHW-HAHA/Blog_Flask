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
from Webapp.forms.user import RegistrationForm, LoginForm, UpdateAccountForm
from Webapp.models import User, Deal, Post, Category
from Webapp import db, bcrypt
import re
import time
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from weixin.login import WeixinLogin
from collections import Counter


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
            return redirect(url_for('webapp.home'))
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
    return render_template('account.html', message = '', title = user.username, user = user, deals = likes_all, total_buys= total_buys, total_likes = total_likes)

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

    return render_template('content_section.html', posts = posts, message = message)


@user_bp.route('/user/edit_account', methods = ['GET', 'POST'])
@login_required # the account page only accessible when ...
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.new_email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('user.account'))
    return render_template('edit_account.html', form = form)


@user_bp.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('webapp.home'))

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















