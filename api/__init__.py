from flask import Flask
from flask_jsonrpc import JSONRPC
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config.from_object(DevConfig)
jsonrpc = JSONRPC(app, '/api')
db = SQLAlchemy(app)
import views


if __name__ == '__main__':
    app.run(port=5001,debug=True)
