#coding:utf-8
from flask import request,session
from utils import validate,write_log
from config import DevConfig
import json,traceback

def auth_login(func):
    def wrapper(*arg, **kwargs):
        try:
            authorization = session['author']
            print authorization
            res = validate(authorization,DevConfig.SECRET_KEY)
            res = json.loads(res)
            if int(res['code']) == 1:
                return json.dumps({'code': 1, 'errmsg': '%s' % res['errmsg']})
        except:
            write_log('api').warning(traceback.format_exc())
            return json.dumps({'code': 1, 'errmsg': '验证异常'})
        return func(res, *arg, **kwargs)
    wrapper.__name__ = '%s_wrapper' % func.__name__
    return wrapper


