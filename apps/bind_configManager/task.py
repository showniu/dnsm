# -*- encoding: utf-8 -*-
# File    : task.py
# Time    : 2020/11/12 10:30 上午
# Author  : ops
from bind_configManager.generate_config import generate_aclViewConf, generate_viewZoneConf, generate_recordConf
from bind_configManager.sync_bindConfig import sync_bindConfig
from celery import shared_task

@shared_task()
def gen_aclViewConf():
    res = generate_aclViewConf()
    return res
@shared_task()
def gen_viewZoneConf():
    res = generate_viewZoneConf()
    return res
@shared_task()
def gen_recordConf():
    res = generate_recordConf()
    return res

# def sync_conf(servers=None, src=None, dest=None, record=None):
#     for server in servers:
#         res = sync_bindConfig(servers=server, src=src, dest=dest, record=record)
#         print(res)



