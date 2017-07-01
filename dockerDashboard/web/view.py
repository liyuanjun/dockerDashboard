# -*- coding: UTF-8 -*-
import commands
import copy
import platform
import threading
import time

from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from dockerDashboard.api import docker_api
from dockerDashboard.tools import funcs
from dockerDashboard.tools.page import pagination
from dockerDashboard.tools.utils import CommonRequest
from dockerDashboard.web.models import DockerHost

DEFAULT_SERVER = None


def docker_hosts(request=None):
    global DEFAULT_SERVER
    data = DockerHost.objects.all()

    if not data:
        DEFAULT_SERVER = None
        return []

    if not request:
        DEFAULT_SERVER = data[0]
        return data

    server = request.COOKIES.get('docker_server')
    if not server:
        DEFAULT_SERVER = data[0]
        return data

    current_servers = filter(lambda x: x.id == int(server), data)
    if not current_servers:
        DEFAULT_SERVER = data[0]
        return data

    DEFAULT_SERVER = current_servers[0]
    current_servers[0].selected = "selected"
    return data


def __default_server(request):
    server = request.COOKIES.get('docker_server')
    global DEFAULT_SERVER

    if DEFAULT_SERVER and server and DEFAULT_SERVER.id == int(server):
        return DEFAULT_SERVER

    docker_hosts(request)
    return DEFAULT_SERVER


def host_list(request):
    data, range, start_index = pagination(request, docker_hosts())
    return render_to_response(
        'dockerHost.html',
        {
            'data': data,
            'page_range': range,
            'start_index': start_index,
            'show_host': True
        }
    )


def host_delete(request, host_id):
    global DEFAULT_SERVER
    if host_id:
        obj = DockerHost.objects.get(id=int(host_id))
        if obj == __default_server(request): DEFAULT_SERVER = None
        obj.delete()
    return HttpResponseRedirect('/host/list')


@csrf_exempt
def host_test(request):
    if platform.system() == 'Windows':
        return JsonResponse({'status': 200, 'msg': '该功能不支持Windows系统！'})

    addr = request.POST.get('ip_addr')
    if not funcs.validate_ip(addr):
        return JsonResponse({'status': 200, 'msg': '请输入正确的ip:port！'})

    status, output = commands.getstatusoutput('curl http://%s/info' % (addr))
    if status == 0:
        return JsonResponse({'status': 200, 'msg': '连接成功！'})
    else:
        return JsonResponse({'status': 200, 'msg': '连接失败！'})


@csrf_exempt
def host_add(request):
    addr = request.POST.get('ip_addr')
    if funcs.validate_ip(addr):
        index = addr.index(':')
        if DockerHost.objects.filter(ip=addr[:index], port=int(addr[index + 1:])).all():
            return JsonResponse({'status': -1, 'msg': '禁止添加重复地址！'})
        DockerHost(ip=addr[:index], port=int(addr[index + 1:])).save()
        return JsonResponse({'status': 200, 'msg': '添加成功！', 'request': '/host/list'})
    return JsonResponse({'status': -1, 'msg': '请输入正确的ip:port！'})


def __bind_images_id(containers):
    bind_images = []
    for con in containers:
        bind_images.append(con.get('ImageID'))

    return bind_images


def __get_container_all(request):
    """
    200 – no error
    400 – bad parameter
    500 – server error
    :return:
    """
    server = __default_server(request)
    if server:
        url = 'http://%s:%d%s' % (server.ip, server.port, docker_api.CONTAINER_ALL)
        code, headers, body = CommonRequest.get(url)
        return body if code == 200 else []
    return []


def __get_images(request):
    server = __default_server(request)
    if server:
        url = 'http://%s:%d%s' % (server.ip, server.port, docker_api.IMAGES_LIST)
        code, headers, body = CommonRequest.get(url)
        return body if code == 200 else []
    return []


def images(request):
    data, image_list = __get_images(request), []
    bind_images = __bind_images_id(__get_container_all(request))

    for obj in data:
        index = 0
        if obj.get('Id') in bind_images:
            obj['used'] = True
        else:
            obj['used'] = False
        obj['Id'] = obj.get('Id')[obj.get('Id').index(':') + 1:]
        obj['Created'] = funcs.time_to_str(obj.get('Created'))
        obj['Size'] = funcs.size_format(obj.get('Size'))

        for tag in obj.get('RepoTags'):
            temp = copy.copy(obj)
            temp['tag'] = tag
            if index > 0: temp['used'] = False
            image_list.append(temp)
            index += 1

    data, range, start_index = pagination(request, image_list)
    return render_to_response(
        'images.html',
        {
            'data': data,
            'page_range': range,
            'start_index': start_index,
            'docker_hosts': docker_hosts(request)
        }
    )


def image_delete(request, image):
    server = __default_server(request)
    url = 'http://%s:%d%s' % (
        server.ip,
        server.port,
        docker_api.IMAGES_DELETE % (image)
    )
    CommonRequest.delete(url=url)
    time.sleep(1)
    return HttpResponseRedirect('/images')


def image_pull(request):
    image = request.GET.get('image')
    server = __default_server(request)

    def pull_request():
        url = 'http://%s:%d%s' % (
            server.ip,
            server.port,
            docker_api.IMAGES_PULL % (image)
        )
        CommonRequest.post(
            url,
            headers={'Content-type': 'application/json'},
            timeout=60 * 30
        )

    threading.Thread(target=pull_request).start()
    return JsonResponse(
        {
            'status': 200,
            'msg': '提示：\n创建中！\n后台默认处理30分钟,超时即失败.',
            'request': '/images/'
        }
    )


def containers(request):
    data = __get_container_all(request)
    for d in data:
        d['Created'] = funcs.time_to_str(d.get('Created'))
        d['Size'] = funcs.size_format(d.get('Size'))
        d['Ports'] = funcs.port_str(d.get('Ports'))

    data, range, start_index = pagination(request, data)
    return render_to_response(
        'containers.html',
        {
            'data': data,
            'page_range': range,
            'start_index': start_index,
            'docker_hosts': docker_hosts(request)
        }
    )


def container_start(request, container):
    server = __default_server(request)
    url = 'http://%s:%d%s' % (
        server.ip,
        server.port,
        docker_api.CONTAINER_START % (container)
    )
    CommonRequest.post(url)
    return HttpResponseRedirect('/containers')


def container_stop(request, container):
    server = __default_server(request)
    url = 'http://%s:%d%s' % (
        server.ip,
        server.port,
        docker_api.CONTAINER_STOP % (container)
    )
    CommonRequest.post(url)

    return HttpResponseRedirect('/containers')


def container_create(request, image):
    server = __default_server(request)
    url = 'http://%s:%d%s' % (
        server.ip,
        server.port,
        docker_api.CONTAINER_CREATE
    )
    CommonRequest.post(
        url=url,
        headers={'Content-type': 'application/json'},
        json=funcs.container_config(image)
    )

    return HttpResponseRedirect('/containers')


def container_create_custom(request):
    """
    Status Codes:   201 – no error
    :param request:
    :return:
    """
    server = __default_server(request)

    url = 'http://%s:%d%s' % (
        server.ip,
        server.port,
        docker_api.CONTAINER_CREATE
    )
    code, headers, body = CommonRequest.post(
        url=url,
        headers={'Content-type': 'application/json'},
        json=funcs.container_config_custom(request)
    )
    if code == 201:
        return JsonResponse({'status': 200, 'msg': '创建成功！', 'request': '/containers'})
    else:
        return JsonResponse({'status': -1, 'msg': body})


@csrf_exempt
def container_create_shell(request):
    server = __default_server(request)
    shell = request.POST.get('shell')

    if '-d' not in shell and '-id' not in shell and '-itd' \
            not in shell and '-td' not in shell and '-tid' not in shell:
        return JsonResponse({'status': -1, 'msg': '不支持交互模式容器，请使用-d参数！'})

    if '\n' in shell:
        shell = shell.replace('\n', ' ')

    if '-H' not in shell:
        shell = shell.replace('docker', 'docker -H %s:%d' % (server.ip, server.port))

    status, output = commands.getstatusoutput(shell)

    if status == 0:
        return JsonResponse({'status': 200, 'msg': '创建成功！', 'request': '/containers'})
    else:
        return JsonResponse({'status': status, 'msg': output})


def container_delete(request, container):
    server = __default_server(request)
    url = 'http://%s:%d%s' % (
        server.ip,
        server.port,
        docker_api.CONTAINER_DELETE % (container)
    )
    CommonRequest.delete(url=url)

    time.sleep(1)
    return HttpResponseRedirect('/containers')


def container_restart(request, container):
    server = __default_server(request)

    url = 'http://%s:%d%s' % (
        server.ip,
        server.port,
        docker_api.CONTAINER_RESTART % (container)
    )
    CommonRequest.post(
        url=url,
        headers={'Content-type': 'application/json'},
    )
    time.sleep(1)
    return HttpResponseRedirect('/containers')
