# coding:utf-8

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from web import  app

db = SQLAlchemy(app)

##用户跟角色关系表
role_user = db.Table('role_user',
                     db.Column('user_id',db.INTEGER,db.ForeignKey('users.id')),
                     db.Column('role_id',db.INTEGER,db.ForeignKey('roles.id'))
                     )

#用户表
class User(db.Model, UserMixin):
    """Represents Proected users"""

    #Set the name for table
    __tablename__ = 'users'
    id = db.Column(db.INTEGER,primary_key=True)
    username = db.Column(db.String(255),comment='用户名')
    password = db.Column(db.String(255),comment='密码')
    name = db.Column(db.String(80), unique=True,comment='姓名',default=username)
    email = db.Column(db.String(64),comment='邮箱')
    mobile = db.Column(db.String(16),comment='手机号码')
    r_id = db.relationship('Role',secondary=role_user, backref=db.backref('roles',lazy='dynamic'), lazy='dynamic')
    is_lock = db.Column(db.Integer,default=0,comment='是否锁定,默认启用,1为锁定')
    join_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow,comment='注册时间')
    last_login = db.Column(db.DateTime, nullable=False,default=datetime.utcnow,comment='最后登录时间')

    def __init__(self,id,username,password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return "<Mode User '{}'>".format(self.username)


#角色表
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.INTEGER,primary_key=True)
    name = db.Column(db.String(20),comment='角色名称',unique=True)
    name_cn = db.Column(db.String(120),comment='角色中文名称s')
    info = db.Column(db.String(120),comment='角色信息')

    def __init__(self, id,name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<Role %r>" % self.name



class Authority(db.Model):
    __tablename__ = 'authoritys'
    id = db.Column(db.INTEGER,autoincrement=True,primary_key=True)
    name = db.Column(db.String(50),comment='权限名称')
    name_cn = db.Column(db.String(100),comment='权限中文名')
    url = db.Column(db.String(128))
    comment = db.Column(db.String(128),comment='备注')


