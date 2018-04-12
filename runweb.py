#!/bin/env python
# -*- encoding: utf-8 -*-
from web import app
from config import DevConfig
import logging

app.config.from_object(DevConfig)

fmter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
handler = logging.FileHandler(DevConfig.WEB_LOGFILE)
handler.setFormatter(fmt=fmter)
app.logger.addHandler(handler)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)