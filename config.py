# coding:utf-8

class Config(object):
    """Base config class."""
    pass

class ProdConfig(Config):
    """Production config class."""
    pass

class DevConfig(Config):
    """Development config class."""
    # Open the DEBUG
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:kbsonlong@btc.frp.along.party:8080/cmdb-flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ##解决the session is unavailable because no secret key was set.错误
    SECRET_KEY='kbsonlong2'
    WEB_LOGFILE='web.log'
    API_LOGFILE='api.log'
    API_HOST='127.0.0.1:5001'
