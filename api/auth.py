#coding:utf-8
from flask import request,session
from utils import validate
from config import DevConfig
import json


def auth_login(func):
    def wrapper(*arg, **kwargs):
        try:
            author = session['author']
            # username = request.args.get('username', None)
            res = validate(author,DevConfig.SECRET_KEY)
            res = json.loads(res)
            #res = {u'username': u'admin', u'code': 0, u'uid': u'1', u'r_id': u'1'}
            if int(res['code']) == 1:
                return json.dumps({'code': 1, 'errmsg': '%s' % res['errmsg']})
            # if res['username'] != username:
            #     return json.dumps({'code': 1, 'errmsg': '验证异常'})
        except:
            return json.dumps({'code': 1, 'errmsg': '验证异常'})
        return func(res, *arg, **kwargs)
    wrapper.__name__ = '%s_wrapper' % func.__name__
    return wrapper

