#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/2 14:08
# @Author  : Tom
# @Site    : 
# @File    : funcs.py
# @Software: dockerDashBoard
import re
import time


def validate_ip(ip_port):
    if ':' in ip_port:
        ip = ip_port[:ip_port.index(':')]
        port = ip_port[ip_port.index(':') + 1:]
        if re.match(u'^([1-9]|'
                    u'[1-9]\\d{1,3}|'
                    u'[1-6][0-5][0-5][0-3][0-5]|'
                    u'[1-5][0-9][0-9][0-9][0-9])$', port) \
                and re.match(
                    u'((?:(?:25[0-5]|'
                    u'2[0-4]\d|((1\d{2})|'
                    u'([1-9]?\d)))\.){3}(?:25[0-5]|'
                    u'2[0-4]\d|'
                    u'((1\d{2})|'
                    u'([1-9]?\d))))', ip):
            return True

    return False


def time_to_str(t):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))


def size_format(b, temp=1000.0):
    if b == 0 or b is '' or b is u'' or b is None:
        return 0
    elif b < temp:
        return '%i' % b + 'B'
    elif temp <= b < temp ** 2:
        return '%.1f' % float(b / temp) + 'KB'
    elif temp ** 2 <= b < temp ** 3:
        return '%.1f' % float(b / temp ** 2) + 'MB'
    elif temp ** 3 <= b < temp ** 4:
        return '%.1f' % float(b / temp ** 3) + 'GB'
    elif temp ** 4 <= b:
        return '%.1f' % float(b / temp ** 4) + 'TB'


def port_str(s):
    """
    :param s: [{u'IP': u'0.0.0.0', u'Type': u'tcp',
              u'PublicPort': 6379, u'PrivatePort': 6379}]
    :return:
    """

    def lam(port):
        if not port.get('PublicPort'):
            return '%d/%s' % (port.get('PrivatePort'), port.get('Type'))

        return '%s:%d->%d/%s' % (port.get('IP'), port.get('PublicPort'),
                                 port.get('PrivatePort'), port.get('Type'))

    return ' '.join(map(lam, s))


def container_config(image):
    param = {
        'Image': image,
        'OpenStdin': True,  # Keep STDIN open even if not attached ==> -i
        'Tty': True,  # Allocate a pseudo-TTY ==> -t
        'StdinOnce': False,  # StdinOnce':False==> -d=true
        'PublishAllPorts': True,
    }
    return param


def container_config_custom(request):
    image = request.GET.get('image')
    start_rule = request.GET.get('start_rule')  # 0 1 2 d it dit
    host_path = request.GET.get('host_path')
    container_path = request.GET.get('container_path')
    host_port = request.GET.get('host_port')
    container_port = request.GET.get('container_port')
    cpu = request.GET.get('cpu')
    memory = request.GET.get('memory')
    cmd = request.GET.get('cmd')
    data = {}

    if start_rule == 0:
        param = {
            'Image': image,
            'OpenStdin': False,
            'Tty': False,
            'StdinOnce': False,
            'PublishAllPorts': True,
            'HostConfig': data
        }
    elif start_rule == 1:
        param = {
            'Image': image,
            'OpenStdin': True,
            'Tty': True,
            'StdinOnce': True,
            'PublishAllPorts': True,
            'HostConfig': data
        }
    else:
        param = {
            'Image': image,
            'OpenStdin': True,
            'Tty': True,
            'StdinOnce': False,
            'PublishAllPorts': True,
            'HostConfig': data
        }

    if host_path and container_path:
        # /opt:/opt/app:ro
        data['Binds'] = [
            '%s:%s' % (host_path, container_path)
        ]

    if host_port and container_port:
        key = '%s/tcp' % container_port

        param['ExposedPorts'] = {
            key: {}
        }
        data['PortBindings'] = {
            key: [
                {'HostIp': '', 'HostPort': '%s' % host_port}
            ]
        }

    if memory:
        data['Memory'] = int(memory) * 1024 * 1024

    if cpu:  # Cpu ==> http://www.open-open.com/news/view/1780c43
        data['CpuPeriod'] = 100000
        data['CpuQuota'] = 10000 * int(float(cpu) * 10)

    if cmd:
        param['Cmd'] = [cmd]

    return param
