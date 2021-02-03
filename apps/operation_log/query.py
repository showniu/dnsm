# -*- encoding: utf-8 -*-
# File    : query.py.py
# Time    : 2020/11/30 下午2:15
# Author  : ops
import json
from bind_server.models import t_bindserver
from bind_service.models import t_bindservice_zone, t_bindservice_record, t_bindservice_aclView
from .models import t_deleteddata_server, t_deleteddata_aclview, t_deleteddata_zone, t_deleteddata_record
from auditlog.models import LogEntry
# 根据ID查询对象属性、针对修改的记录后来被删除、数据表中没有被删除的记录
'''
t_bindservice_aclView 的查询方式是查询操作表里面的删除记录、删除记录里面包含了删除的内容；
其他的model也可以使用这方方法；这个办法是中途想出来的；前面的先不改了、暂时两种方法并存吧；
action='2' 是从删除的记录中寻找被删除数据的信息；
'''
def objId_query(objType=None, object_repr=None, objId=None):
    if objType == 't_bindserver':
        # print('对象ID', objId)
        query_data = t_bindserver.objects.filter(id=objId).values()

        if query_data.exists():
            m_res = {}
            m_res['plat_server_ip'] = query_data[0]['plat_server_ip']
            m_res['plat_server_init'] = query_data[0]['plat_server_init']

            return m_res
        else:
            # 当数据表中不存在该条数据时、就从删除记录中获取这个记录的信息
            his_data = LogEntry.objects.filter(object_repr=object_repr, action='2').values('changes')
            his_server_ip = (json.loads(his_data[0]['changes']))['plat_server_ip'][0]
            his_server_init = (json.loads(his_data[0]['changes']))['plat_server_init'][0]

            h_res = {}
            h_res['plat_server_ip'] = his_server_ip
            h_res['his_server_init'] = his_server_init

            return h_res

    elif objType == 't_bindservice_aclView':
        query_data = t_bindservice_aclView.objects.filter(id=objId).values()

        if query_data.exists():
            m_res = {}
            m_res['acl_name'] = query_data[0]['acl_name']
            m_res['acl_value'] = query_data[0]['acl_value']

            return m_res
        else:
            # 根据object_repr 和action 定位是哪个资源；（假定数据表中不存在的数据一定是被正常手段删除。并且有删除记录）
            his_data = LogEntry.objects.filter(object_repr=object_repr, action='2').values('changes')
            his_acl_name = (json.loads(his_data[0]['changes']))['acl_name'][0]
            his_acl_value = (json.loads(his_data[0]['changes']))['acl_value'][0]

            h_res = {}
            h_res['acl_name'] = his_acl_name
            h_res['acl_value'] = his_acl_value

            return h_res

    elif objType == 't_bindservice_zone':
        query_data = t_bindservice_zone.objects.filter(id=objId).values()
        if query_data.exists():
            m_res = {}
            m_res['zone_name'] = query_data[0]['zone_name']
            m_res['zone_from_view'] = query_data[0]['zone_from_view']

            return m_res
        else:
            his_data = LogEntry.objects.filter(object_repr=object_repr, action='2').values('changes')
            his_zone_name = (json.loads(his_data[0]['changes']))['zone_name'][0]
            his_zone_from_view = (json.loads(his_data[0]['changes']))['zone_from_view'][0]

            h_res = {}
            h_res['zone_name'] = his_zone_name
            h_res['zone_from_view'] = his_zone_from_view

            return h_res



    elif objType == 't_bindservice_record':
        query_data = t_bindservice_record.objects.filter(id=objId).values()
        # 在 model 查找数据
        if query_data.exists():
            record_key_prefix = query_data[0]['record_key']
            record_key_suffix = query_data[0]['record_zone']

            # 一条DNS记录的关键信息、这些信息要体现在一条修改日志里、才能定位到被操作的具体数据
            record_key = record_key_prefix + '.' + record_key_suffix
            record_value = query_data[0]['record_value']
            record_from_view = query_data[0]['record_from_view']
            record_type = query_data[0]['record_type']

            m_res = {}
            m_res['record_key'] = record_key
            m_res['record_value'] = record_value
            m_res['record_form_view'] = record_from_view
            m_res['record_type'] = record_type

            return m_res
        # 从删除的记录中查找数据的信息
        else:
            his_data = LogEntry.objects.filter(object_repr=object_repr, action='2').values('changes')

            his_record_key_prefix = (json.loads(his_data[0]['changes']))['record_key'][0]
            his_record_key_suffix = (json.loads(his_data[0]['changes']))['record_zone'][0]

            his_record_key = his_record_key_prefix + '.' + his_record_key_suffix
            his_object_value = (json.loads(his_data[0]['changes']))['record_value'][0]
            his_object_view = (json.loads(his_data[0]['changes']))['record_from_view'][0]
            his_record_type = (json.loads(his_data[0]['changes']))['record_type'][0]

            h_res = {}
            h_res['record_key'] = his_record_key
            h_res['record_value'] = his_object_value
            h_res['record_form_view'] = his_object_view
            h_res['record_type'] = his_record_type

            return h_res
    else:
        return 'objType 必填'
