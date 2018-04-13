#coding:utf-8
from flask import render_template,redirect, url_for,request,session
from web import app
from flask_jsonrpc import JSONRPC
import requests,json
from config import DevConfig
from utils import validate

jsonrpc = JSONRPC(app, '/api')
headers = {'content-type': 'application/json'}

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
        url = "http://%s/api/login?username=%s&passwd=%s" % (DevConfig.API_HOST, username, password)
        print url
        r = requests.get(url, headers=headers)  # 请求API验证用户，并获取token
        result = json.loads(r.content)
        print result
        if result['code'] == 0:
            session['username'] = username
            session['author'] = result['authorization']
            headers['authorization'] = session['author']
            return redirect(url_for('home'))
        elif result['code'] == 1:
            info = result['errmsg']
    return render_template('WEB/login.html',info = info ,username = username)

@app.route('/')
@app.route('/index')
# @login_required
def home():
    """View function for home page"""
    if 'username' in session:
        username = session['username']
        authorization = session['author']
        return render_template('WEB/index.html', username=username)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))


#zabbix 监控
@app.route('/zabbix/<htmlname>')
def zabbix(htmlname):
    print session['author']
    if session.get('author','nologin') == 'nologin':
        return redirect('/login')
    headers['authorization'] = session['author']
    validate_result = json.loads(validate(session['author'], DevConfig.SECRET_KEY))
    url = "http://%s/api/zbhost" % '127.0.0.1:5001'
    r = requests.get(url, headers=headers)
    result = json.loads(r.content)
    if int(validate_result['code']) == 0:

        return render_template('WEB/'+htmlname+'.html',info=session,username=session['username'])
    else:
        return render_template('WEB/'+htmlname+'.html',errmsg=validate_result['errmsg'])