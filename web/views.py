#coding:utf-8
from flask import render_template,redirect, url_for,request,session
from web import app
from models import User,db


@app.route('/login',methods=['POST','GET'])
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
            session['username'] = username
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

    if 'username' in session:
        username = session['username']
        print username
        return render_template('WEB/index.html', username=username)

    return render_template('WEB/login.html')