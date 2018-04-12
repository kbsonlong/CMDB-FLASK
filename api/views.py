# coding:utf-8

from flask import request,session,redirect,url_for
from api import app
from models import db,User
import json,time
from auth import auth_login
from utils import write_log,get_validate
from config import DevConfig


@app.route('/api/login', methods=['GET'])
def login():
    """View function for home page"""
    # 判断是否是验证提交
    write_log('api').warning('test')
    try:
        username = request.args.get('username', None)
        password = request.args.get('passwd', None)

        if not (username and password):
            return json.dumps({'code': 1, 'errmsg': "需要输入用户名和密码"})
        user = db.session.query(User).filter_by(username = username).first()
        passwd = db.session.query(User).filter_by(username=username, password=password).first()
        if not user:
            return json.dumps({'code': 1, 'errmsg': "用户不存在"})

        if user.is_lock == 1:
            return json.dumps({'code': 1, 'errmsg': "用户已被锁定"})

        if passwd:
            data = {'last_login': time.strftime('%Y-%m-%d %H:%M:%S')}
            db.session.query(User).update(data)
            db.session.commit()
            token = get_validate(user.username,DevConfig.SECRET_KEY)
            return json.dumps({'code': 0, 'authorization': token})
        else:
            return json.dumps({'code': 1, 'errmsg': "输入密码有误"})
    except:
        return json.dumps({'code': 1, 'errmsg': "登录失败"})


@app.route('/api/get_user')
@auth_login
def get_user(user,**kwargs):
    return json.dumps({})