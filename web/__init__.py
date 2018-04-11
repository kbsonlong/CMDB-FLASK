# coding:utf-8
from flask import Flask,redirect,url_for
from config import DevConfig
app = Flask(__name__)

cmdb_logger = app.logger

import views
