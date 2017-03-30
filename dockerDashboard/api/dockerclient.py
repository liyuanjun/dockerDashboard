#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/6/30 22:52
# @Author  : Tom
# @Desc    : use docker remote api 1.9
# @File    : dockerClient.py
# @Software: dockerDashBoard
# docs     : http://www.phperz.com/article/15/0911/155461.html

import requests
import json


class _DictAble(object):
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


class DockerClient(object):
    """
    docker client
    """

    def __init__(self, ip, port=2375):
        self.ip = ip
        self.port = port
        self.url = 'http://%s:%s' % (self.ip, self.port)


class Images(DockerClient):
    """
    docker 镜像
    """
    IMAGES_LIST = '/images/json'  # GET /images/json?all=0
    IMAGES_SEARCH = '/images/search?term=%s'  # GET  /images/search?term=ssh  (dockerhub repo)
    IMAGES_BUILD = '/build'  # POST /build   (param is a tar file include Dockerfile)
    IMAGES_DELETE = '/images/%s'  # DELETE /images/(name)
    IMAGES_COMMIT = '/commit'  # POST /commit?container=44c004db4b17&m=message&repo=myrepo
    IMAGES_CREATE = '/images/create'  # POST /images/create?fromImage=base
    IMAGES_PUSH = '/images/%s/push'  # POST /images/(name)/push
    IMAGES_PULL = '/images/create?fromImage=%s'  # POST /images/create?fromImage=base
    IMAGES_INFO = '/images/%s/history'  # GET /images/(name)/history
    IMAGES_INSPECT = '/images/%s/json'  # GET /images/(name)/json
    IMAGES_INSERT = '/images/%s/insert'  # POST /images/(name)/insert?path=/usr&url=myurl

    @_DictAble.decorator
    def list(self, term=None):
        if term:
            url = self.url + self.IMAGES_SEARCH % term
        else:
            url = self.url + self.IMAGES_LIST
        return requests.get(url)

    def build(self):
        pass

    @_DictAble.decorator
    def delete(self, name):
        url = self.url + self.IMAGES_DELETE % name
        return requests.delete(url)

    @_DictAble.decorator
    def create(self, from_image=None, from_src=None, repo=None, tag=None, registry=None):
        """ docker.io/kingaric/2048 ==> registry/repo/from_image
        :param from_image:  name of the image to pull
        :param from_src: source to import, - means stdin
        :param repo: repository
        :param tag: tag
        :param registry: the registry to pull from
        :return:
                200 – no error
                500 – server error
        """
        url, data = self.url + self.IMAGES_CREATE, {}
        if from_image:
            data['fromImage'] = from_image
        else:
            data['from_src'] = from_src
        if repo:
            data['repo'] = repo
        if tag:
            data['tag'] = tag
        if registry:
            data['registry'] = registry
        return requests.post(url, data=data)

    def push(self):
        pass

    def pull(self):
        pass


class Containers(DockerClient):
    pass
