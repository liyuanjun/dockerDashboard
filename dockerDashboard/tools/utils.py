#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/2 14:08
# @Author  : Tom
# @Site    : 
# @File    : utils.py
# @Software: dockerDashBoard
import logging

import requests


class DictAble(object):
    @staticmethod
    def decorator(func):
        def wrapper(*args, **kwargs):
            code, headers, body = 500, {}, 'server error'
            try:
                res = func(*args, **kwargs)
                code, headers, body = res.status_code, res.headers, res.json()
            except Exception, e:
                logging.error('[ %s method ] error: %s' % (func.__name__, e))
                logging.error(code,body)
            return code, headers, body

        return wrapper


class CommonRequest(object):
    @staticmethod
    @DictAble.decorator
    def get(url, params=None, **kwargs):
        return requests.get(url, params=params, **kwargs)

    @staticmethod
    @DictAble.decorator
    def post(url, data=None, json=None, **kwargs):
        return requests.post(url, data=data, json=json, **kwargs)

    @staticmethod
    @DictAble.decorator
    def delete(url, **kwargs):
        return requests.delete(url,**kwargs)
