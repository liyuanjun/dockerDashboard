#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/6/30 22:52
# @Author  : Tom
# @Desc    : use docker remote api 1.9
# @File    : dockerClient.py
# @Software: dockerDashBoard
# docs     : http://www.phperz.com/article/15/0911/155461.html
from .containers import Containers
from .images import Images

class DockerClient(object):
    """
    docker client
    """
    def __init__(self,host,port=2375):
        self.images = Images(host,port)
        self.containers = Containers(host,port)









