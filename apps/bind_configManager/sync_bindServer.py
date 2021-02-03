# -*- encoding: utf-8 -*-
# File    : sync_bindConfig.py
# Time    : 2020/10/27 3:26 下午
# Author  : ops
import os
from pathlib import Path
from fabric2 import SerialGroup, ThreadingGroup, runners, Connection
from celery import shared_task
from .models import t_bindconf_tag

current_dir = os.getcwd()
app_dir = current_dir + '/apps/bind_configManager'
download_dir = app_dir + '/get_conf'
download_conf_dir = download_dir + '/ops-dnsm-bind-config'

'''
Connection.put() 只能copy单独的文件、并且只能操作一台服务器

'''

@shared_task()
def sync_OpsBindConfig(server=None, src=None, dest=None, record=None):
    connect_key = {'key_filename': '/Users/lxxjp/.ssh/id_rsa.bak'}
    dir_cmd = 'mkdir -p ' + dest

    # 创建目录
    with Connection(server, user='root', connect_kwargs=connect_key) as chostConnect:
        dir_result = chostConnect.run(dir_cmd)

    if dir_result.ok:
        print(dir_cmd + '; ' + "目录创建成功")
        if record:
            scp_cmd_record = "scp -r " + src + "/*.host " + "root@" + server + ":" + dest
            t = os.system(scp_cmd_record)
            return (scp_cmd_record, t)
        else:
            scp_cmd_zoneView = "scp " + src + " " + "root@" + server + ":" + dest
            y = os.system(scp_cmd_zoneView)
            return (scp_cmd_zoneView, y)




# 下载远程配置文件
@shared_task()
def git_get_config(tag=None):
    print('检查本地代码是否存在', download_dir)
    # 当前目录是否存在项目目录
    project_dir_re = Path(download_conf_dir)
    if project_dir_re.is_dir():
        print('目录已存在、删除')
        # 如果存在就拉取一下最新的配置、返回命令执行状态
        re = os.system('rm -rf ' + download_conf_dir)


    print('目录不存在', download_conf_dir)
    git_clone_cmd = 'git clone ' + ' --branch ' + tag \
                    + ' ssh://git@gitlab.xxxx.com:2222/jiapeng.li/ops-dnsm-bind-config.git ' \
                    + download_conf_dir
    print('下载配置到本地', git_clone_cmd)
    re = os.system(git_clone_cmd)
    return re


# 同步远程配置文件
@shared_task()
def sync_bindConfig(opServer=None, noOpserver=None, tag_id=None):
    # 服务器目录
    bind9_basicConfig_dir = '/usr/local/bind9/etc/'
    bind9_acl_dir = bind9_basicConfig_dir + 'acl/'
    bind9_viewZone_dir = bind9_basicConfig_dir + 'viewZone/'
    bind9_record_dir = bind9_basicConfig_dir + 'hostRecord/'

    # 本地目录 download_conf_dir
    # 同步命令、并更新数据库、标签的状态
    res = []
    for server in opServer:
        res_dict = {}
        mkdir_cmd = 'ssh root@' + server + ' ' + 'mkdir -p ' + bind9_acl_dir + ' ' + bind9_viewZone_dir + ' ' + bind9_record_dir
        rsync_acl_cmd = 'rsync -avd --delete ' + download_conf_dir + '/acl/acl.conf ' + "root@" + server + ":" + bind9_acl_dir
        rsync_view_cmd = 'rsync -avd --delete ' + download_conf_dir + '/viewZone/view.conf ' + "root@" + server + ":" + bind9_viewZone_dir
        rsync_host_cmd = 'rsync -avd --delete ' + download_conf_dir + '/hostRecord/ ' + "root@" + server + ":" + bind9_record_dir
        os.system(mkdir_cmd)
        sync_acl = os.system(rsync_acl_cmd)
        sync_view = os.system(rsync_view_cmd)
        sync_host = os.system(rsync_host_cmd)

        if sync_acl == 0 and sync_view == 0 and sync_host == 0:
            res_dict['type'] = 'success'
            res_dict['info'] = server + ':' + '已部署'
        else:
            res_dict['type'] = 'danger'
            res_dict['info'] = server + ':' + '部署失败'

        res.append(res_dict)
    if noOpserver:
        for server in noOpserver:
            res_dict = {}
            res_dict['type'] = 'success'
            res_dict['info'] = server + ':' + '已部署'
            res.append(res_dict)

    print('tyx', res)
    t_bindconf_tag.objects.filter(id=tag_id).update(tag_currentstatus=res)

    return res

# if __name__ == '__main__':
#     # src = '/Users/ljp/Documents/zhilian/gitlab/dnsm/apps/bind_configManager/output_conf/view.conf'
#     src = '/Users/ljp/Documents/zhilian/gitlab/dnsm/apps/bind_configManager/output_conf/'
#     dest = '/usr/local/bind9/etc/acl'
#     server = '10.10.10.2'
#     s = sync_OpsBindConfig(server=server, src=src, dest=dest, record=True)
#     print(s)
