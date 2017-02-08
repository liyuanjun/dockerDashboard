# -*- coding: UTF-8 -*-

from django.db import models

"""
    sqlite
"""


class DockerHost(models.Model):
    id = models.AutoField(primary_key=True)  # pk
    ip = models.CharField(max_length=50, null=False)
    port = models.IntegerField(null=False)

    class Meta:
        db_table = 't_docker_host'
