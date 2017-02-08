# -*- coding: UTF-8 -*-

import httplib
import urllib


default_timeout = 5

# urllib.urlencode({}) ==> urllib.quote_plus(str({}))

def get_req(**kwargs):
    status = None
    http_client = None
    data = None
    try:
        http_client = httplib.HTTPConnection(
            kwargs.get('host'), kwargs.get('port'), timeout=default_timeout)

        if kwargs.get('params'):
            params = '?' + urllib.urlencode(kwargs.get('params'))
        else:
            params = ''

        http_client.request('GET', kwargs.get('url') + params)
        response = http_client.getresponse()
        status = response.status
        data = response.read()

    except Exception, e:
        print e
    finally:
        if http_client:
            http_client.close()
        return status, data


def post_req(**kwargs):
    status = None
    http_client = None
    data = None
    try:
        timeout=default_timeout
        if kwargs.get('timeout'):timeout= kwargs.get('timeout')
        http_client = httplib.HTTPConnection(
            kwargs.get('host'), kwargs.get('port'), timeout=timeout)
        http_client.request(
            method='POST', url=kwargs.get('url'), body=kwargs.get('body'), headers=kwargs.get('headers'))
        response = http_client.getresponse()
        status = response.status
        data = response.read()

    except Exception, e:
        print 'http post error :{0}'.format(e)
    finally:
        if http_client:
            http_client.close()
        return status, data

def delete_req(**kwargs):
    status = None
    http_client = None
    data = None
    try:
        http_client = httplib.HTTPConnection(
            kwargs.get('host'), kwargs.get('port'), timeout=default_timeout)
        http_client.request(
            method='DELETE', url=kwargs.get('url'))
        response = http_client.getresponse()
        status = response.status
        data = response.read()

    except Exception, e:
        print 'http post error :{0}'.format(e)
    finally:
        if http_client:
            http_client.close()
        return status, data