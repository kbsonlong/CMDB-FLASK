# coding:utf-8
import logging,os,logging.config,time,base64,hashlib,json,traceback

def write_log(loggername):
    work_dir = os.path.dirname(os.path.realpath(__file__))
    log_conf= os.path.join(work_dir, 'conf','logger.conf')
    logging.config.fileConfig('logger.conf')
    logger = logging.getLogger(loggername)
    return logger

def get_validate(username, fix_pwd):
    t = int(time.time())
    print t
    validate_key = hashlib.md5('%s%s%s' % (username, t, fix_pwd)).hexdigest()
    return base64.b64encode('%s|%s|%s' % (username, t,validate_key)).strip()


def validate(key, fix_pwd):
    t = int(time.time())
    key = base64.b64decode(key)
    x = key.split('|')
    if len(x) != 3:
        write_log('api').warning('Errmsg:token参数不足\n%s' % traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'token参数不足'})
    if t > int(x[1]) + 2*60*60:
        write_log('api').warning('errmsg:登录已过期\n%s' % traceback.format_exc() )
        return json.dumps({'code':1,'errmsg':'登录已过期'})
    validate_key = hashlib.md5('%s%s%s' % (x[0], x[1], fix_pwd)).hexdigest()
    print validate_key
    if validate_key == x[2]:
        return json.dumps({'code':0,'username':x[0],'token':x[2]})
    else:
        write_log('api').warning('errmsg:密码不正确\n%s' % traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'密码不正确'})