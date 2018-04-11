#coding:utf-8
from flask import Blueprint,render_template,redirect,flash,url_for,request
import urllib2,ssl,json
from models import User,db
from web import app


@app.route('/login',methods=('POST','GET'))
def login():
    """View function for home page"""
    context={}
    info =''
    username = ''
    # 判断是否是验证提交
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.session.query(User).filter_by(username = username).all()
        passwd = db.session.query(User).filter_by(username=username, password=password).all()
        if user and passwd:
                return redirect(url_for('home'))
        elif not user:
            info = 'please check username'
        else:
            info = 'please check password'
    return render_template('WEB/login.html',info = info ,username = username)

@app.route('/')
# @login_required
def home():
    """View function for home page"""
    username='kbsonlong'
    return render_template('WEB/index.html',username = username)