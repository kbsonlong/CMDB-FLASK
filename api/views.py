# coding:utf-8

from flask import request,session,redirect,url_for
from api import app
from models import db,User
import json,time,traceback
from auth import auth_login
from utils import write_log,get_validate
from config import DevConfig


@app.route('/api/login', methods=['GET'])
def login():
    """View function for home page"""
    # 判断是否是验证提交
    try:
        username = request.args.get('username', None)
        password = request.args.get('passwd', None)

        if not (username and password):
            write_log('api').warning('errmsg:需要输入用户名和密码\n%s' % traceback.format_exc())
            return json.dumps({'code': 1, 'errmsg': "需要输入用户名和密码"})
        user = db.session.query(User).filter_by(username = username).first()
        if not user:
            write_log('api').warning('errmsg:用户不存在\n%s' % traceback.format_exc())
            return json.dumps({'code': 1, 'errmsg': "用户不存在"})

        if user.is_lock == 1:
            write_log('api').warning('errmsg:用户已被锁定\n%s' % traceback.format_exc())
            return json.dumps({'code': 1, 'errmsg': "用户已被锁定"})

        if user.verify_password(password):
            data = {'last_login': time.strftime('%Y-%m-%d %H:%M:%S')}
            User.query.filter_by(username=username).update(data)
            db.session.commit()
            token = get_validate(user.username,DevConfig.SECRET_KEY)
            return json.dumps({'code': 0, 'authorization': token})
        else:
            write_log('api').warning('errmsg:输入密码有误\n%s' % traceback.format_exc())
            return json.dumps({'code': 1, 'errmsg': "输入密码有误"})
    except:
        write_log('api').warning('errmsg:登录失败\n%s' % traceback.format_exc() )
        return json.dumps({'code': 1, 'errmsg': "登录失败"})


@app.route('/api/get_user')
@auth_login
def get_user(auth_info,**kwargs):
    return json.dumps({'code' : 0 ,'authorization': auth_info['token']})