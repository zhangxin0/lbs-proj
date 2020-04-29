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
    response = make_response(json.dumps(resp))
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
    return response

@route_user.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        return ops_render("user/edit.html", {'current': 'edit'})
    resp = {'code': 200, 'msg': 'success', 'data': {}}
    req = request.values
    nickname = req['nickname'] if 'nickname' in req else ''
    email = req['email'] if 'email' in req else ''

    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = 'Please input nickname in good format'
        return jsonify(resp)
    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = 'Please input email in good format'
        return jsonify(resp)

    # Store info to db
    user_info = g.current_suer
    user_info.nickname = nickname
    user_info.email = email

    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)


@route_user.route("/reset-pwd", methods=["GET", "POST"])
def resetPwd():
    if request.method == "GET":
        return ops_render("user/reset_pwd.html", {'current': 'reset'})
    resp = {'code': 200, 'msg': 'success', 'data': {}}
    req = request.values
    old_password = req['old_password'] if 'old_password' in req else ''
    new_password = req['new_password'] if 'new_password' in req else ''
    user_info = g.current_user
    if UserService.genePwd(old_password, user_info.login_salt) != user_info.login_pwd:
        resp['code'] = -1
        resp['msg'] = 'Please input right old password'
        return jsonify(resp)
    user_info.login_pwd = UserService.genePwd(new_password, user_info.login_salt)
    db.session.add(user_info)
    db.session.commit()

    # update cookie:
    response = make_response(json.dumps(resp))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], '%s#%s' % (UserService.geneAuthCode(user_info), user_info.uid),
                        60 * 60 * 24 * 120)  # save for 120 days
    return response


@route_user.route('/logout')
def logout():
    response = make_response(redirect(UrlManager.buildUrl('/user/login')))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response


