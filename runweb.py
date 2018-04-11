#!/bin/env python
# -*- encoding: utf-8 -*-
from web import app
from config import DevConfig
app.config.from_object(DevConfig)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)