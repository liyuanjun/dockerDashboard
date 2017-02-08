# -*- coding: UTF-8 -*-
"""
Status Codes:
204 – no error
404 – no such container
500 – server error

"""
DOCKER_INFO = '/info'  # GET
DOCKER_VERSION = '/version'  # GET

# IMAGES
IMAGES_LIST = '/images/json'  # GET
IMAGES_SEARCH = '/images/search?term=%s'  # GET  /images/search?term=ssh  (dockerhub repo)
IMAGES_BUILD = '/build'  # POST /build   (param is a tar file include Dockerfile)
IMAGES_DELETE = '/images/%s'  # DELETE /images/(name)
IMAGES_CREATE = '/commit'  # POST /commit?container=44c004db4b17&m=message&repo=myrepo
IMAGES_PUSH='/images/%s/push' #POST /images/(name)/push
IMAGES_PULL='/images/create?fromImage=%s' #POST /images/create?fromImage=base
IMAGES_INFO='/images/%s/history' #GET /images/(name)/history
IMAGES_INSPECT='/images/%s/json' #GET /images/(name)/json
IMAGES_INSERT='/images/%s/insert' #POST /images/(name)/insert?path=/usr&url=myurl

# CONTAINER
CONTAINER_LIST = '/containers/json'  # GET
CONTAINER_ALL = '/containers/json?all=1'  # GET
CONTAINER_CREATE = '/containers/create'  # POST
CONTAINER_START = '/containers/%s/start'  # POST /containers/(id)/start
CONTAINER_STOP = '/containers/%s/stop'  # POST /containers/(id)/stop?t=5  (t is kill time)
CONTAINER_RESTART = '/containers/%s/restart' #POST  /containers/(id)/restart?t=5
CONTAINER_DELETE = '/containers/%s'  # DELETE /containers/(id)?v=1
