# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, make_response, redirect, g
from common.models.User import User
from common.libs.Helper import ops_render
from common.libs.user.UserService import UserService
import json
from application import app, db
from common.libs.UrlManager import UrlManager

route_user = Blueprint('user_page', __name__)

@route_user.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return ops_render("user/login.html")
    resp = {'code': 200, 'msg': 'Login Success!', 'data': {}}
    req = request.values
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    user_info = User.query.filter_by(user_name=login_name).first()
    if not user_info:
        resp['code'] = -1
        resp['msg'] = 'username not exists！'
        return jsonify(resp)

    if user_info.password != login_pwd:
        resp['code'] = -1
        resp['msg'] = 'Incorrect username or password！'
        return jsonify(resp)
    # make_response 制作请求头 make_response可以返回内容，json序列化的和返回界面render_template('')
    response = make_response(json.dumps(resp))
    # cookie名字和参数
    response.set_cookie(app.config['AUTH_COOKIE_NAME'],"%s#%s"%(UserService.geneAuthCode(user_info),user_info.id))
    return response

@route_user.route("/register", methods=["GET"])
def register():
    return ops_render("user/register.html")

@route_user.route("/register_submit", methods=["POST"])
def register_submit():
    resp = {'code': 200, 'msg': 'Login Success!', 'data': {}}
    req = request.values
    user = User()
    # 判断用户明是否存在：
    res = User.query.filter_by(user_name=req['user_name']).first()
    if res:
        resp['code'] = -1
    else:
        # sqlachemy
        user.user_name = req['user_name']
        user.password = req['password']
        user.email = req['email']
        user.first_name = req['first_name']
        user.middle_name = req['middle_name']
        user.last_name = req['last_name']
        user.mail_address = req['mail_address']
        user.phone_number = req['phone_number']
        user.occupation = req['occupation']
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            app.logger.info(e)
    response = make_response(resp)
    # 更新cookie为新用户cookie，完成新用户登陆，防止旧用户cookie登陆
    if resp['code'] == 200:
        g.current_user = User.query.filter_by(user_name=user.user_name).first()
        response.set_cookie(app.config['AUTH_COOKIE_NAME'],"%s#%s"%(UserService.geneAuthCode(g.current_user),g.current_user.id))
    return response

@route_user.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        return ops_render("user/edit.html")
    resp = {'code': 200, 'msg': 'Login Success!', 'data': {}}
    req = request.values
    # 判断用户是否存在：
    res = User.query.filter_by(user_name=req['user_name']).first()
    user = User.query.filter_by(id=g.current_user.id).first()
    if res:
        resp['code'] = -1
    else:
        # sqlachemy
        user.user_name = req['user_name']
        user.email = req['email']
        user.first_name = req['first_name']
        user.middle_name = req['middle_name']
        user.last_name = req['last_name']
        user.mail_address = req['mail_address']
        user.phone_number = req['phone_number']
        user.occupation = req['occupation']
        try:
            db.session.commit()
        except Exception as e:
            app.logger.info(e)
    response = make_response(resp)
    # 修改完用户信息后，重置cookie，不然会自动退出：
    if resp['code'] == 200:
        g.current_user = User.query.filter_by(user_name=user.user_name).first()
        response.set_cookie(app.config['AUTH_COOKIE_NAME'],"%s#%s"%(UserService.geneAuthCode(g.current_user),g.current_user.id))
    return response


@route_user.route("/reset-pwd", methods=["GET", "POST"])
def resetPwd():
    if request.method == "GET":
        return ops_render("user/reset_pwd.html")
    resp = {'code': 200, 'msg': 'success', 'data': {}}
    req = request.values
    old_password = req['old_password'] if 'old_password' in req else ''
    new_password = req['new_password'] if 'new_password' in req else ''
    user_info = g.current_user
    if old_password != user_info.password:
        resp['code'] = -1
        resp['msg'] = 'Please input right old password!'
        return jsonify(resp) # dict json序列化为对象
    user_info.password = new_password
    db.session.commit()

    # update cookie:
    response = make_response(json.dumps(resp))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], '%s#%s' % (UserService.geneAuthCode(user_info), user_info.id),
                        60 * 60 * 24 * 120)  # save for 120 days
    return response


@route_user.route('/logout')
def logout():
    response = make_response(redirect(UrlManager.buildUrl('/user/login')))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response


