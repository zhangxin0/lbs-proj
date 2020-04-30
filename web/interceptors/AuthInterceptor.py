from application import app
from flask import request, redirect, g
from common.models.User import User
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
import re


@app.before_request
def before_request():
    ignore_urls = app.config['IGNORE_URLS']
    ignore_check_login_urls = app.config['IGNORE_CHECK_LOGIN_URLS']
    path = request.path
    pattern = re.compile('%s' % '|'.join(ignore_check_login_urls))
    if pattern.match(path):
        return
    user_info = check_login()
    g.current_user = None
    if user_info:
        g.current_user = user_info
    # re.compile https://docs.python.org/3/library/re.html
    pattern = re.compile('%s' % '|'.join(ignore_urls))
    if pattern.match(path):
        return
    if not user_info:
        return redirect(UrlManager.buildUrl("/user/login"))
    return

# Cookie通过末尾的uid得到数据库中的user信息，生成正确的cookie值，与request中的cookie值做双向验证
def check_login():
    # cookie在登陆完成时已经设置好 cookie: name=...
    cookies = request.cookies
    auth_cookie = cookies[app.config['AUTH_COOKIE_NAME']] if app.config['AUTH_COOKIE_NAME'] in cookies else None
    if auth_cookie is None:
        return False
    auth_info = auth_cookie.split('#')
    if len(auth_info) != 2:
        return False
    try:
        user_info = User.query.filter_by(id=int(auth_info[1])).first()
    except Exception as e:
        print(e)
        return False

    if user_info is None:
        return False
    # cookie是用户名和密码生成的唯一值，这里相当于对用户信息进行了校验
    if auth_info[0] != UserService.geneAuthCode(user_info):
        return False

    return user_info
