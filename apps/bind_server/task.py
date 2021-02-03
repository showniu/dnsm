# -*- encoding: utf-8 -*-
# File    : bindServerInit.py
# Time    : 2020/10/28 7:07 下午
# Author  : ops
# 教程     : https://fabric-chs.readthedocs.io/zh_CN/chs/tutorial.html
import json
from fabric2 import Connection
import time
from .models import t_bindserver
from .serializers import BindServerSerializer
import socket, paramiko.ssh_exception
from fabric2 import SerialGroup, ThreadingGroup, runners
from fabric2.exceptions import GroupException
from celery import shared_task

def updateDb_tServer(serverIp=None, state=None):
    resdata = t_bindserver.objects.get(plat_server_ip=serverIp)
    mdData = {}
    mdData['plat_server_init'] = state
    c = BindServerSerializer(resdata, mdData, partial=True)
    if c.is_valid():
        c.save()
    return c.data

@shared_task()
def opsServerInit(servers=None):
    connect_key = {'key_filename': '/Users/ljp/.ssh/id_rsa.bak'}
    # 操作单台服务器
    # hostConnect = Connection(host='10.10.10.131', user='root', connect_kwargs=connect_key)

    # 批量操作服务器、串行或并行
    # 串行
    # chostConnect = SerialGroup('10.10.10.130', '10.10.10.131', user='root', connect_kwargs=connect_key)

    # 并行
    bhostConnect = ThreadingGroup(*servers, user='root', connect_kwargs=connect_key)
    try:
        cmd = 'hostname'
        result = bhostConnect.run(cmd, hide=True)
        print('sss', result)
        # 组装执行结果
        opsCmdLog = []
        for con, res in result.items():
            resDict = {}
            hostIp = con.host
            resOut = res.stdout.strip()
            resDict['serverIp'] = hostIp
            resDict['resOut'] = resOut
            opsCmdLog.append(resDict)
            updateDb_tServer(serverIp=con.host, state='2')
        print(opsCmdLog)
        return opsCmdLog
    except GroupException as e:
        opsCmdLog = []
        for c, r in e.result.items():
            print(c, r)
            resDict = {}
            resDict['serverIp'] = c.host
            print('x', r)
            if isinstance(r, runners.Result):
                resOut = r.stdout.strip()
                resDict['resOut'] = resOut
                updateDb_tServer(serverIp=c.host, state='2')
            elif isinstance(r, socket.gaierror):
                resOut = 'FAILED,  Network error'
                resDict['resOut'] = resOut
                resDict['initState'] = '3'
                updateDb_tServer(serverIp=c.host, state='3')
            elif isinstance(r, paramiko.ssh_exception.AuthenticationException):
                resOut = 'FAILED,  Auth failed'
                resDict['resOut'] = resOut
                resDict['initState'] = '3'
                updateDb_tServer(serverIp=c.host, state='3')
            else:
                resOut = ', 主机无法通信或者其他问题'
                resDict['resOut'] = str(r) + resOut
                resDict['initState'] = '3'
                updateDb_tServer(serverIp=c.host, state='3')
            opsCmdLog.append(resDict)
        # time.sleep(30)
        print(opsCmdLog)
        return opsCmdLog

'''
server_list = ['10.10.10.130', '10.10.10.131', '10.10.10.132']
# server_list = ','.join(server_list)
server_listLen = len(server_list)
hosts = ''
for key in range(server_listLen):
    host = server_list[key]
    if key == 0:
        hosts = '\'' + host + '\''
    else:
        hosts = hosts + ', ' + '\'' + host + '\''
'''


# a = ['10.10.10.130', '10.10.10.131', '10.10.10.132']
# print(opsServerInit(a))
