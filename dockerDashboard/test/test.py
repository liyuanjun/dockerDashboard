# a={'a':123}
# c=a
# c['uu']=''
# print a
#
#
# import copy
# a={'a':123}
# d=copy.copy(a)
# d['uu']=''
# print a

##################
# port = [{u'IP': u'0.0.0.0', u'Type': u'tcp', u'PublicPort': 6379, u'PrivatePort': 6379},
#         {u'IP': u'0.0.0.0', u'Type': u'tcp', u'PublicPort': 6379, u'PrivatePort': 6379}]
# res = []
# for i in port:
#     if i.get('PublicPort'):
#         res.append('%s:%d->%d/%s' % (i.get('IP'), i.get('PublicPort'), i.get('PrivatePort'), i.get('Type')))
#     else:
#         res.append('%d/%s' % (i.get('PrivatePort'), i.get('Type')))
# print ' '.join(res)

##################
# import json
#
# aa={'ImageID': 'bb11232a492cee4fddc718ea0ae37e5f814499154685204da1aaf3e2d5cdc320'}
# print json.dumps(aa)


##################
# import json
# a='[{"RepoDigests": null,"Created":1466711701,"Size":5042677,"VirtualSize":5042677,"Labels":null}]'
# a=json.loads(a)
# print a


# a='[{"RepoDigests": null,"Created":1466711701,"Size":5042677,"VirtualSize":5042677,"Labels":null}]'
# b= eval(a)
# print b

# a='[{"RepoDigests": null,"Created":1466711701,"Size":5042677,"VirtualSize":5042677,"Labels":null}]'
# c={}
# exec('c='+a)
# print c

##################
import commands, os
# (status, output) = commands.getstatusoutput('curl http://192.168.137.14:2375/info')
# print status
# print os.system("docker run -d  7a131b11cf190")

###################
# s='1:2'
# index=s.index(':')
# print ''
# print s[:index]
# print s[index+1:]

###################
# import re
# print re.match(u'^([1-9]|[1-9]\\d{1,3}|[1-6][0-5][0-5][0-3][0-5]|[1-5][0-9][0-9][0-9][0-9])$','23751')
# print re.match(u'((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))','0.0.0.0')


###################

# os.system("export DOCKER_HOST='tcp://192.168.137.147:2375'")
# os.system(shell+" '192.168.137.147:2375' 'docker ps'" )
# strs='docker \nps'
# if '\n' in strs:strs= strs.replace('\n',' ')
# if '-H' not in strs:
#     strs= strs.replace('docker','docker -H 192.168.137.147:2375')
# print strs
# print  commands.getstatusoutput(strs)
