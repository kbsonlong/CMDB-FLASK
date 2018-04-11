# coding:utf-8

from flask import request,session,redirect,url_for
from api import app
from models import db,User
import json,time,traceback,hashlib,base64
from auth import validate

def get_validate(username, password):
    t = int(time.time())
    validate_key = hashlib.md5('%s%s%s' % (username, t, password)).hexdigest()
    return base64.b64encode('%s|%s|%s' % (username, t,validate_key)).strip()

@app.route('/api/login', methods=['GET'])
def login():
    """View function for home page"""
    # 判断是否是验证提交
    try:
        username = request.args.get('username', None)
        password = request.args.get('passwd', None)
        print username,password
        if not (username and password):
            return json.dumps({'code': 1, 'errmsg': "需要输入用户名和密码"})
        user = db.session.query(User).filter_by(username = username).first()
        print user
        passwd = db.session.query(User).filter_by(username=username, password=password).first()
        if not user:
            return json.dumps({'code': 1, 'errmsg': "用户不存在"})

        if user.is_lock == 1:
            return json.dumps({'code': 1, 'errmsg': "用户已被锁定"})
        print passwd

        if passwd:
            data = {'last_login': time.strftime('%Y-%m-%d %H:%M:%S')}
            print data
            db.session.query(User).update(data)
            db.session.commit()
            token = get_validate(user.username,user.password)
            return json.dumps({'code': 0, 'authorization': token})
        else:
            return json.dumps({'code': 1, 'errmsg': "输入密码有误"})
    except:
        return json.dumps({'code': 1, 'errmsg': "登录失败"})
