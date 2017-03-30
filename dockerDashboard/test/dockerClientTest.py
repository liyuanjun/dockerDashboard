#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/30 23:17
# @Author  : Tom
# @Site    : 
# @File    : dockerClientTest.py
# @Software: dockerDashBoard

from dockerDashboard.api import dockerclient

image = dockerclient.Images('192.168.137.147')

print image.create(from_image='2048',repo='kingaric')







