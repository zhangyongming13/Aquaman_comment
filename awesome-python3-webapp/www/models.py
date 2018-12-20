#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time, uuid
from orm import Model, StringField, BooleanField, FloatField, TextField


def next_id():
    # 自动生成ID
    return '%15d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class User(Model)