#!/bin/env python
# -*- encoding: utf-8 -*-
from api import app
from config import DevConfig
app.config.from_object(DevConfig)


if __name__ == '__main__':
    app.run(port=5001)