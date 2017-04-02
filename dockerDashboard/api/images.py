#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/2 14:06
# @Author  : Tom
# @Site    : 
# @File    : Images.py
# @Software: dockerDashBoard
import requests
from ..tools.utils import DictAble


class Images(object):
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

    def __init__(self, ip, port=2375):
        self.ip = ip
        self.port = port
        self.url = 'http://%s:%s' % (self.ip, self.port)

    @DictAble.decorator
    def list(self, term=None):
        if term:
            url = self.url + self.IMAGES_SEARCH % term
        else:
            url = self.url + self.IMAGES_LIST
        return requests.get(url)

    def build(self):
        pass

    @DictAble.decorator
    def delete(self, name):
        url = self.url + self.IMAGES_DELETE % name
        return requests.delete(url)

    @DictAble.decorator
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