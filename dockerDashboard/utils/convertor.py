import json
import time
import re

'''
utils
'''


def validate_ip(ip_port):
    if ':' in ip_port:
        ip = ip_port[:ip_port.index(':')]
        port = ip_port[ip_port.index(':') + 1:]
        if re.match(u'^([1-9]|[1-9]\\d{1,3}|[1-6][0-5][0-5][0-3][0-5]|[1-5][0-9][0-9][0-9][0-9])$', port) \
                and re.match(
                    u'((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))',
                    ip):
            return True
    return False


def transfer(s):
    return json.loads(s)


def transfer_reverse(s):
    return json.dumps(s)


def time_to_str(t):
    t = time.localtime(t)
    return time.strftime('%Y-%m-%d %H:%M:%S', t)


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
    [{u'IP': u'0.0.0.0', u'Type': u'tcp', u'PublicPort': 6379, u'PrivatePort': 6379}]
    :param s:
    :return:
    """
    res = []
    for i in s:
        if i.get('PublicPort'):
            res.append('%s:%d->%d/%s' %
                       (i.get('IP'), i.get('PublicPort'), i.get('PrivatePort'), i.get('Type')))
        else:
            res.append('%d/%s' % (i.get('PrivatePort'), i.get('Type')))
    return ' '.join(res)


def container_config(image):
    param = {'Image': image,
             'OpenStdin': True,  # Keep STDIN open even if not attached ==> -i
             'Tty': True,  # Allocate a pseudo-TTY ==> -t
             'StdinOnce': False,  # StdinOnce':False==> -d=true
             'PublishAllPorts': True,
             }
    return json.dumps(param)


def container_config_custom(request):
    image = request.GET.get('image')
    start_rule = request.GET.get('start_rule')  # 0 1 2 d it dit
    host_path = request.GET.get('host_path')
    container_path = request.GET.get('container_path')
    host_port = request.GET.get('host_port')
    container_port = request.GET.get('container_port')
    cpu = request.GET.get('cpu')
    memery = request.GET.get('memery')
    cmd = request.GET.get('cmd')
    data={}
    if start_rule == 0:
        param = {'Image': image,
                 'OpenStdin': False,
                 'Tty': False,
                 'StdinOnce': False,
                 'PublishAllPorts': True,
                 'HostConfig':data
                 }
    elif start_rule == 1:
        param = {'Image': image,
                 'OpenStdin': True,
                 'Tty': True,
                 'StdinOnce': True,
                 'PublishAllPorts': True,
                 'HostConfig': data
                 }
    else:
        param = {'Image': image,
                 'OpenStdin': True,
                 'Tty': True,
                 'StdinOnce': False,
                 'PublishAllPorts': True,
                 'HostConfig': data
                 }
    if host_path and container_path:
        # /opt:/opt/app:ro
        data['Binds']=[
                 '%s:%s' % (host_path, container_path)
        ]
    if host_port and container_port:
        param['ExposedPorts'] = {
            '%s/tcp' % (container_port): {}
        }
        data['PortBindings'] = {
            '%s/tcp' % (container_port): [{'HostIp': '', 'HostPort': '%s' % (host_port)}]
        }

    if memery:
        data['Memory'] = int(memery) * 1024 * 1024
    if cpu:  # Cpu ==> http://www.open-open.com/news/view/1780c43
        data['CpuPeriod'] = 100000
        data['CpuQuota'] = 10000 * int(float(cpu) * 10)
    if cmd:
        param['Cmd'] = [cmd]

    return json.dumps(param)
