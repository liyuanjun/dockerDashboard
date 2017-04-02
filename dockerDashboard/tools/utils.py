#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/2 14:08
# @Author  : Tom
# @Site    : 
# @File    : utils.py
# @Software: dockerDashBoard
import json
class DictAble(object):
    @staticmethod
    def decorator(func):
        def wrapper(*args, **kwargs):
            code, headers, body = 500, {}, 'server error'
            try:
                res = func(*args, **kwargs)
                code, headers, body = res.status_code, res.headers, json.loads(res.content)
            except Exception, e:
                print '%s method error: %s' % (func.__name__, e)
            return code, headers, body

        return wrapper