

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
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://kbsonlong:kbsonlong@192.168.137.153:3306/cmdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    port = 5001
