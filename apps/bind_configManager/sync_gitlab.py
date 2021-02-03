# -*- encoding: utf-8 -*-
# File    : sync_gitlab.py
# Time    : 2020/12/14 上午11:02
# Author  : ops

import django
import gitlab
import os
import time
from celery import shared_task
from celery import chain
from pathlib import Path
from .setializers import BindConfTagSerializer
from bind_configManager.models import t_bindconf_tag
from bind_configManager.generate_config import generate_aclViewConf, generate_viewZoneConf, generate_recordConf

# django.setup()

current_dir = os.getcwd()
app_dir = current_dir + '/apps/bind_configManager'
out_dir = app_dir + '/output_conf'
project_dir = app_dir + '/ops-dnsm-bind-config'
aclConf_dir = project_dir + '/acl'
viewConf_dir = project_dir + '/viewZone'
hostConf_dir = project_dir + '/hostRecord/'

# 移动生成配置文件到项目目录
@shared_task()
def move_conf():
    print('本地目录移动')
    if not os.listdir(out_dir):
        # 基本不会发生这个情况、因为配置生成和上传是前后进行的
        return out_dir + ' 目录为空, 生成配文件的目录为空、请生成配置后再'
    else:
        print(os.listdir(out_dir))
        os.system('mkdir -p ' + aclConf_dir + ' ' + viewConf_dir + ' ' + hostConf_dir)

        mv_acl = os.system('rsync -avd --delete ' + out_dir + '/acl/acl.conf ' + aclConf_dir)
        mv_view = os.system('rsync -avd --delete ' + out_dir + '/viewZone/view.conf ' + viewConf_dir)
        mv_host = os.system('rsync -avd --delete ' + out_dir + '/hostRecord/ ' + hostConf_dir)
        print('配置移动结果', type(mv_acl), mv_view, mv_host)

        if mv_acl == 0 and mv_host == 0 and mv_view == 0:
            rm_cmd = 'rm -rf ' + out_dir + '/*'
            print(rm_cmd)
            os.system(rm_cmd)

        res = {}
        res['mv_acl'] = mv_acl
        res['mv_view'] = mv_view
        res['mv_host'] = mv_host
        return res

# 克隆远程配置到本地
@shared_task()
def clone_pull_gitlab():
    print('检查本地代码是否存在', project_dir)
    # 当前目录是否存在项目目录
    project_dir_re = Path(project_dir)
    if project_dir_re.is_dir():
        print('目录已存在、拉取远程最新配置')
        # 如果存在就拉取一下最新的配置、返回命令执行状态
        re = os.system('cd ' + project_dir + ' && '
                       'pwd && '
                       'git pull')
        return re
    else:
        # 目录不存在则说明、需要clone项目到本地、
        print('目录不存在', project_dir)
        git_clone_cmd = 'git clone ssh://git@gitlab.xxxxx.com:2222/jiapeng.li/ops-dnsm-bind-config.git'

        re = os.system('cd ' + app_dir + ' && '
                       + git_clone_cmd)
        return re

# push 本地修改
@shared_task()
def push_gitlab():
    print('提交到gitlab')
    tagname_suffic = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
    tagname = 'master-v0.0.0-' + str(tagname_suffic)
    push_cmd = 'git add --all && git commit -m ' + tagname + ' && git push origin master'
    push_tag_cmd = 'git tag -a ' + tagname + ' -m ' + tagname + ' && git push origin ' + tagname
    print('push命令', push_cmd)
    push_re = os.system('cd ' + project_dir + ' && pwd && ' + push_cmd)
    print('push结果', push_re)
    if push_re == 0:
        print('tag push', push_tag_cmd)
        os.system('cd ' + project_dir + ' && pwd && ' + push_tag_cmd)
    return push_re

@shared_task()
def build_conf():
    acl = generate_aclViewConf()
    viewZone = generate_viewZoneConf()
    record = generate_recordConf()

    return (acl, viewZone, record)

@shared_task()
def get_project_tags():
    gl = gitlab.Gitlab('https://gitlab.xxxx.com', 'Token')
    # project = gl.projects.list(search='ops-dnsm-bind-config')

    project = gl.projects.get('4917') #项目ID
    project_tags = project.tags.list()
    db_tagList = t_bindconf_tag.objects.values_list('tag_name', flat=True)

    tag_list = []
    for tag in project_tags:
        print('处理tag', tag)
        print(tag.name)
        data = {}
        data['tag_name'] = tag.name
        data['tag_test'] = None
        data['tag_related_server'] = None
        data['tag_currentstatus'] = None
        save_data = BindConfTagSerializer(data=data)

        if save_data.is_valid() and tag.name not in db_tagList:
            save_data.save()
            tag_list.append(tag.name)
        else:
            print('没有新tag产生')

    return tag_list

