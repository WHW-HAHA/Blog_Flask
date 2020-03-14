import re
import time
import requests
from flask import Flask, render_template, session, jsonify

app = Flask(__name__)
app.secret_key = '1231sdfasdf'

from bs4 import BeautifulSoup


def xml_parse(text):
    result = {}
    soup = BeautifulSoup(text, 'html.parser')
    tag_list = soup.find(name='error').find_all()
    for tag in tag_list:
        result[tag.name] = tag.text
    return result


@app.route('/login')
def login():
    ctime = int(time.time() * 1000)
    qcode_url = "https://login.wx2.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_={0}".format(
        ctime)

    rep = requests.get(
        url=qcode_url
    )
    # print(rep.text) # window.QRLogin.code = 200; window.QRLogin.uuid = "gb8UuMBZyA==";
    qcode = re.findall('uuid = "(.*)";', rep.text)[0]
    session['qcode'] = qcode
    return render_template('login.html', qcode=qcode)


@app.route('/check/login')
def check_login():
    qcode = session['qcode']
    ctime = int(time.time() * 1000)
    # https://login.wx2.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid=oeq3xdRFig==&tip=0&r=-412057997&_=1546600257051
    # https://login.wx2.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid=oa95cvIS5w==&tip=0&r=-413943228&_=1546602155746
    check_login_url = 'https://login.wx2.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}&tip=0&r=-413943228&_={1}'.format(
        qcode, ctime)
    rep = requests.get(
        url=check_login_url
    )
    result = {'code': 408}

    if 'window.code=408' in rep.text:
        # 用户未扫码
        result['code'] = 408
    elif 'window.code=201' in rep.text:
        # 用户扫码，获取头像
        result['code'] = 201
        result['avatar'] = re.findall("window.userAvatar = '(.*)';", rep.text)[0]
    elif 'window.code=200' in rep.text:
        # 用户确认登录
        redirect_uri = re.findall('window.redirect_uri="(.*)";', rep.text)[0]
        print(redirect_uri)

        # https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=A_pgPh0SjvyHWTDEF3kce2Wg@qrticket_0&uuid=wbewGl1rwQ==&lang=zh_CN&scan=1546599481&fun=new&version=v2
        # https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=A_pgPh0SjvyHWTDEF3kce2Wg@qrticket_0&uuid=wbewGl1rwQ==&lang=zh_CN&scan=15

        redirect_uri = redirect_uri + "&fun=new&version=v2"
        ru = requests.get(url=redirect_uri)

        # <error><ret>0</ret><message></message><skey>@crypt_2272b9c9_c4a1df2d806c0b32bc7f8b678b907bd6</skey><wxsid>hKPtRPRAn0yZWwZW</wxsid><wxuin>1440810436</wxuin><pass_ticket>%2BuiXaDx68luSpK5djbIrAqKoVLi4vSlxTg7dQe4105vIaFK93ORlG1kPgO5uQsSi</pass_ticket><isgrayscale>1</isgrayscale></error>
        ticket_dict = xml_parse(ru.text)
        # print(ticket_dict)
        session['ticket_dict'] = ticket_dict
        print('this is the ticket_dict {0}'.format(session['ticket_dict']))
        result['code'] = 200

    return jsonify(result)


@app.route('/index')
def index():
    pass_ticket = session['ticket_dict']['pass_ticket']
    init_url = "https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-412030554&lang=zh_CN&pass_ticket={0}".format(
        pass_ticket)

    rep = requests.post(
        url=init_url,
        json={
            'BaseRequest': {
                'DeviceID': "e572672200373583",
                'Sid': session['ticket_dict']['wxsid'],
                'Skey': session['ticket_dict']['skey'],
                # 'Uin': session['ticket_dict']['wxuin'],
                'Uin': "1440810436",

            }
        }
    )
    rep.encoding = 'utf-8'

    init_user_dict = rep.json()
    print(init_user_dict)

    return render_template('index.html', init_user_dict=init_user_dict)


if __name__ == '__main__':
    app.run()
