

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
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:kbsonlong@along_db:33060/cmdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    port = 5001
