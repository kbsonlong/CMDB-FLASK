#coding:utf-8
from flask import request
from . import app
import json,traceback,time,base64,hashlib



def validate(key, fix_pwd):
    t = int(time.time())
    key = base64.b64decode(key)
    x = key.split('|')
    print x
    if len(x) != 3:
        return json.dumps({'code':1,'errmsg':'token参数不足'})
    if t > int(x[1]) + 2*60*60:
        return json.dumps({'code':1,'errmsg':'登录已过期'})
    validate_key = hashlib.md5('%s%s%s' % (x[0], x[1], fix_pwd)).hexdigest()
    print validate_key
    if validate_key == x[4]:
        return json.dumps({'code':0,'username':x[0],'uid':x[2],'r_id':x[3]})
    else:
        return json.dumps({'code':1,'errmsg':'密码不正确'})


def auth_login(func):
    def wrapper(*arg, **kwargs):
        try:
            authorization = request.headers.get('authorization', 'None')
            res = validate(authorization, app.config['passport_key'])
            res = json.loads(res)
            #res = {u'username': u'admin', u'code': 0, u'uid': u'1', u'r_id': u'1'}
            if int(res['code']) == 1:
                return json.dumps({'code': 1, 'errmsg': '%s' % res['errmsg']})
        except:
            return json.dumps({'code': 1, 'errmsg': '验证异常'})
        return func(res, *arg, **kwargs)
    wrapper.__name__ = '%s_wrapper' % func.__name__
    return wrapper

