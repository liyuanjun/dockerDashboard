#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-5-5 上午3:21
# @Author  : tom.lee
# @Site    : 
# @File    : test.py
# @Software: PyCharm


import requests

from dockerDashboard.api import docker_api

DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 2375

param = {
    'Image': 'kingaric/redis:latest',
    'OpenStdin': True,  # Keep STDIN open even if not attached -i
    'Tty': True,  # Allocate a pseudo-TTY -t
    'StdinOnce': False,  # StdinOnce':False== -d=true
    'PublishAllPorts': True,
    'HostConfig': {
        'Binds': [
            '/opt:/opt/app',
            '/vol:/vol/app:ro'
        ],
        'PortBindings': {
            '6379/tcp': [{'HostIp': '', 'HostPort': '16379'}]
        },
        'CpuPeriod': 100000,
        'CpuQuota': 100000,
    }
}


def create_container(param):
    url = 'http://192.168.137.147:2375' + docker_api.CONTAINER_CREATE
    print requests.post(url=url, json=param)


