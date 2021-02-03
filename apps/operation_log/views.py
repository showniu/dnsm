from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from rest_framework import status
from rest_framework import generics

from auditlog.models import LogEntryManager
from auditlog.models import LogEntry
from .query import objId_query
from bind_server.models import t_bindserver

# Create your views here.

class OperationsLog(APIView):
    def get(self, *args, **kwargs):
        data = LogEntry.objects.all()
        # 查询 acl和view的修改
        # data = LogEntry.objects.filter(changes__icontains="acl_value")

        res_list = []
        for instance in data:
            # 操作表中的变动记录详情、json 形式记录
            instance_changes = json.loads(instance.changes)
            res_history_dict = {}
            # 第一层判断、区分操作动作
            # 创建
            res_history_dict['time'] = instance.timestamp
            if instance.action == 0:
                # 第二次判断、区分操作的数据对象
                object_dbModel = (instance.object_repr).split(' ')[0]
                if object_dbModel == 't_bindserver':
                    # server_name = instance_changes['plat_server_hostname'][1]
                    server_ip = instance_changes['plat_server_ip'][1]
                    # server_port = instance_changes['plat_server_port'][1]
                    # res_history_dict['action'] = 0
                    # res_history_dict['object_type'] = 'server'
                    # res_history_dict['server_name'] = server_name
                    # res_history_dict['server_ip'] = server_ip
                    # res_history_dict['server_port'] = server_port
                    res_history_dict['msg'] = "新增 服务器 IP为 " + server_ip

                elif object_dbModel == 't_bindservice_aclView':
                    line_name = instance_changes['acl_name'][1]
                    line_range = instance_changes['acl_value'][1]
                    # res_history_dict['action'] = 0
                    # res_history_dict['object_type'] = 'line'
                    # res_history_dict['line_name'] = line_name
                    # res_history_dict['line_range'] = line_range
                    res_history_dict['msg'] = '新增 线路 ' + line_name + ' 线路范围为 ' + line_range

                elif object_dbModel == 't_bindservice_zone':
                    zone_name = instance_changes['zone_name'][1]
                    zone_from_view = instance_changes['zone_from_view'][1]
                    zone_type = instance_changes['zone_type'][1]
                    # res_history_dict['action'] = 0
                    # res_history_dict['object_type'] = 'zone'
                    # res_history_dict['zone_name'] = zone_name
                    # res_history_dict['zone_from_view'] = zone_from_view
                    # res_history_dict['zone_type'] = zone_type
                    if zone_type == 'forward':
                        zone_forwarders = instance_changes['zone_forwarders'][1]
                        # res_history_dict['zone_forwards'] = zone_forwarders
                        res_history_dict['msg'] = '新增 转发域名 ' + zone_name \
                                                  + ' 线路 ' + zone_from_view \
                                                  + ' 目标服务器 ' + zone_forwarders
                    else:
                        res_history_dict['msg'] = '新增 主域名 ' + zone_name + ' 线路 ' + zone_from_view
                elif object_dbModel == 't_bindservice_record':
                    record_key = instance_changes['record_key'][1]
                    record_type = instance_changes['record_type'][1]
                    record_value = instance_changes['record_value'][1]

                    record_from_view = instance_changes['record_from_view'][1]
                    record_zone = instance_changes['record_zone'][1]
                    # res_history_dict['action'] = 0
                    # res_history_dict['object_type'] = 'record'
                    # res_history_dict['record_key'] = record_key
                    # res_history_dict['record_type'] = record_type
                    # res_history_dict['record_value'] = record_value
                    # res_history_dict['record_zone'] = record_zone
                    # res_history_dict['record_from_view'] = record_from_view
                    res_history_dict['msg'] = '新增 解析记录 ' \
                                              + record_type + '记录 ' \
                                              + record_key + '.' + record_zone + ' ' \
                                              + ' 线路 ' + record_from_view + ' ' \
                                              + ' 解析值 ' + record_value

            # 修改
            elif instance.action == 1:
                # 获取操作的对象类型、就是那些Model
                object_dbModel = (instance.object_repr).split(' ')[0]
                object_repr = instance.object_repr
                if object_dbModel == 't_bindserver':
                    # 服务器数据无法修改、但是有初始状态可以修改
                    object_id = instance.object_id
                    server_data = objId_query('t_bindserver', object_repr, object_id)
                    # res_history_dict['action'] = 1
                    # res_history_dict['object_type'] = 'server'
                    # res_history_dict['plat_server_ip'] = server_data['plat_server_ip']

                    # 这里应该做判断、但是server只有一个字段可以被修改、所以直接赋值即可
                    # res_history_dict['plat_server_init'] = instance_changes['plat_server_init']
                    old_server_init = instance_changes['plat_server_init'][0]
                    new_server_init = instance_changes['plat_server_init'][1]

                    init_dict = {
                        'None': '未初始化',
                        '0': '未初始化',
                        '1': '初始化中',
                        '2': '已初始化',
                        '3': '初始化失败'
                    }
                    # print(init_dict[old_server_init], type(init_dict[old_server_init]))
                    res_history_dict['msg'] = '修改 服务器 ' + server_data['plat_server_ip'] + ' 状态 ' + init_dict[old_server_init] + '(' + old_server_init + ')' \
                                              + ' 改为 ' + init_dict[new_server_init] + '(' + new_server_init + ')'

                elif object_dbModel == 't_bindservice_aclView':
                    object_id = instance.object_id
                    res_history_dict['action'] = 1
                    res_history_dict['object_type'] = 'aclView'
                    line_data = objId_query('t_bindservice_aclView', object_repr, object_id)

                    # res_history_dict['acl_name'] = line_data['acl_name']
                    # res_history_dict['acl_value'] = instance_changes['acl_value']
                    res_history_dict['msg'] = '修改 线路 ' + line_data['acl_name'] \
                                              + ' 线路范围 ' + instance_changes['acl_value'][0] \
                                              + ' 改为 线路范围 ' + instance_changes['acl_value'][1]

                elif object_dbModel == 't_bindservice_zone':
                    object_id = instance.object_id
                    res_history_dict['action'] = 1
                    res_history_dict['object_type'] = 'zone'
                    zone_data = objId_query('t_bindservice_zone', object_repr, object_id)

                    # zone只有zone_from_view是可以修改的、其他的不能修改、所以直接赋值即可
                    # res_history_dict['zone_name'] = zone_data['zone_name']
                    # res_history_dict['zone_from_view'] = instance_changes['zone_from_view']
                    res_history_dict['msg'] = '修改 域名 ' + zone_data['zone_name'] \
                                              + ' 线路 ' + instance_changes['zone_from_view'][0] \
                                              + ' 改为 ' + instance_changes['zone_from_view'][1]

                elif object_dbModel == 't_bindservice_record':
                    object_id = instance.object_id
                    res_history_dict['action'] = 1
                    res_history_dict['object_type'] = 'record'

                    # 取这条修改记录的更多信息、可能是从 model 或者操作记录表中的 删除记录中 取到
                    record_data = objId_query('t_bindservice_record', object_repr, object_id)

                    # 设定各个字段的默认值(这是)
                    # instance_changes 中只有被修改的字段、其他字段是没有的、所以需要预定义
                    # res_history_dict['record_key'] = [record_data['record_key'], record_data['record_key']]
                    # res_history_dict['record_type'] = [record_data['record_type'], record_data['record_type']]
                    # res_history_dict['record_value'] = [record_data['record_value'], record_data['record_value']]
                    # res_history_dict['record_from_view'] = [record_data['record_form_view'], record_data['record_form_view']]

                    # res_history_dict['record_ttl'] = record_data['record_ttl']

                    # 判断可修改的字段是否被修改（在instance_changes中存在的字段即被修改）、并重新赋值、覆盖上面的预定义

                    # 只有 record_value 被修改
                    if 'record_value' in instance_changes:
                        res_history_dict['msg'] = '修改 解析记录 ' + record_data['record_type'][0] + '记录 ' \
                                                  + record_data['record_key'] \
                                                  + ' 线路' + record_data['record_form_view'] \
                                                  + ' 解析值' + instance_changes['record_value'][0] \
                                                  + ' 改为 ' + record_data['record_type'][0] + '记录 ' \
                                                  + record_data['record_key'] \
                                                  + ' 线路' + record_data['record_form_view'] \
                                                  + ' 解析值' + instance_changes['record_value'][1]
                    # record_type 、record_value 同时被修改
                    if 'record_type' in instance_changes and 'record_value' in instance_changes:
                        res_history_dict['msg'] = '修改 解析记录 ' + instance_changes['record_type'][0] + '记录 ' \
                                                  + record_data['record_key'] \
                                                  + ' 线路' + record_data['record_form_view'] \
                                                  + ' 解析值' + instance_changes['record_value'][0] \
                                                  + ' 改为 ' + instance_changes['record_type'][1] + '记录 ' \
                                                  + record_data['record_key'] \
                                                  + ' 线路' + record_data['record_form_view'] \
                                                  + ' 解析值' + instance_changes['record_value'][1]

                    # if 'record_remark' in instance_changes:
                    #     res_history_dict['record_remark'] = instance_changes['record_remark']

                    # if 'record_ttl' in instance_changes:
                    #     res_history_dict['record_ttl'] = instance_changes['record_ttl']


            # 删除
            elif instance.action == 2:
                object_dbModel = (instance.object_repr).split(' ')[0]
                if object_dbModel == 't_bindserver':
                    # 如果服务器被删除、直接取服务器IP显示被删除即可
                    # res_history_dict['action'] = 2
                    # res_history_dict['object_type'] = 'server'
                    # res_history_dict['server_ip'] = instance_changes['plat_server_ip'][0]
                    res_history_dict['msg'] = '删除 服务器 IP为 ' + instance_changes['plat_server_ip'][0]

                elif object_dbModel == 't_bindservice_aclView':
                    # res_history_dict['action'] = 2
                    # res_history_dict['object_type'] = 'aclView'
                    # res_history_dict['acl_name'] = instance_changes['acl_name'][0]
                    res_history_dict['msg'] = '删除 线路 ' + instance_changes['acl_name'][0]
                elif object_dbModel == 't_bindservice_zone':
                    # res_history_dict['action'] = 2
                    # res_history_dict['object_type'] = 'zone'
                    # res_history_dict['zone_name'] = instance_changes['zone_name'][0]
                    res_history_dict['msg'] = '删除 域名 ' + instance_changes['zone_name'][0]
                elif object_dbModel == 't_bindservice_record':
                    res_history_dict['action'] = 2
                    res_history_dict['object_type'] = 'record'

                    record_key_prefix = instance_changes['record_key'][0]
                    record_key_suffix = instance_changes['record_zone'][0]
                    rrecord_key = record_key_prefix + '.' + record_key_suffix
                    # res_history_dict['record_type'] = instance_changes['record_type'][0]
                    # res_history_dict['record_value'] = instance_changes['record_value'][0]
                    # res_history_dict['record_from_view'] = instance_changes['record_from_view'][0]
                    res_history_dict['msg'] = '删除 域名 ' + rrecord_key

            res_list.append(res_history_dict)

        responseData = {}
        responseData['total'] = len(res_list)
        responseData['data'] = res_list
        return Response(responseData)

'''
CREATE = 0
UPDATE = 1
DELETE = 2
        
新增 解析记录 CNAME记录 msou                 默认 waf.zhaopin.com  ( TTL: 600)
新增 解析记录 A记录     dpl.dev.zhaopin.com  默认 192.168.11.68    ( TTL: 120) 

删除 解析记录 CNAME记录 apiapp  中国地区_华南 waf6.zhaopin.com  ( TTL: 60)
删除 解析记录 A记录     lb-gray 默认         59.151.7.34       ( TTL: 60)

修改 解析记录 CNAME记录 api 默认 waf6.zhaopin.com ( TTL: 600, 权重: 1) 改为 CNAME记录 api 默认 wafv6.zhaopin.com (TTL:600, 权重: 1)

'''
