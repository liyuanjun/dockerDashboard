#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/2 14:06
# @Author  : Tom
# @Site    : 
# @File    : Containers.py
# @Software: dockerDashBoard

import requests
from ..tools.utils import DictAble


class Containers(object):
    CONTAINER_LIST = '/containers/json'  # GET
    CONTAINER_ALL = '/containers/json?all=1'  # GET
    CONTAINER_CREATE = '/containers/create'  # POST
    CONTAINER_START = '/containers/%s/start'  # POST /containers/(id)/start
    CONTAINER_STOP = '/containers/%s/stop'  # POST /containers/(id)/stop?t=5  (t is kill time)
    CONTAINER_RESTART = '/containers/%s/restart' #POST  /containers/(id)/restart?t=5
    CONTAINER_DELETE = '/containers/%s'  # DELETE /containers/(id)?v=1

    def __init__(self, ip, port=2375):
        self.ip = ip
        self.port = port
        self.url = 'http://%s:%s' % (self.ip, self.port)

    @DictAble.decorator
    def list(self,alls=True):
        if alls:
            url = self.url+self.CONTAINER_ALL
        else:
            url = self.url + self.CONTAINER_LIST
        return requests.get(url)

    def create(self):
        url = self.url + self.CONTAINER_CREATE
        return requests.post(url)

    def delete(self,container):
        url = self.url + self.CONTAINER_DELETE % container
        return requests.delete(url)

    def start(self,container):
        url = self.url + self.CONTAINER_START % container
        return  requests.post(url)

    def stop(self,container):
        url = self.url + self.CONTAINER_STOP % container
        return requests.post(url)

    def restart(self,conatiner):
        url= self.url + self.CONTAINER_RESTART % conatiner
        return requests.post(url)