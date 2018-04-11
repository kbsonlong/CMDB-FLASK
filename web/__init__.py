# coding:utf-8
from flask import Flask,redirect,url_for
from config import DevConfig
from flask_jsonrpc import JSONRPC
app = Flask(__name__)
app.config.from_object(DevConfig)
cmdb_logger = app.logger

import views
