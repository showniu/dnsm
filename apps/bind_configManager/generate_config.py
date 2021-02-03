# -*- coding: utf-8 -*
# 创建日期： 2020-10-03 20:40
# 文件名：generate_config.py
import django
import os
from celery import shared_task
django.setup()


from jinja2 import PackageLoader, Environment
from bind_service.models import t_bindservice_aclView, t_bindservice_zone, t_bindservice_record

current_dir = os.getcwd()
env = Environment(loader=PackageLoader('conf_template'))
acl_template = env.get_template("acl_template.conf")
viewAndZone_template = env.get_template("viewAndZone_template.conf")
record_template = env.get_template("record_template.conf")
# bind9_SysBasicConfig_dir = '/usr/local/bind9/etc/'
# bind9_basicConfig_dir = '/Users/ljp/data/bind9/etc/'
bind9_basicConfig_dir = '/usr/local/bind9/etc/'
bind9_viewZone_dir = bind9_basicConfig_dir + 'viewZone/'
bind9_record_dir = bind9_basicConfig_dir + 'hostRecord/'
build_out_dir = current_dir + '/apps/bind_configManager/output_conf/'
aclConf_save_path = build_out_dir + 'acl/'
viewZoneSavePath = build_out_dir + 'viewZone/'
record_confSave_path = build_out_dir + 'hostRecord/'

def generate_conf(temp_def=None, save_path=None, data=None):
    content = temp_def.render(datas=data)
    os.system('mkdir -p ' + os.path.dirname(save_path))
    with open(save_path, 'w') as f:
        f.write(content)
    return save_path

# 生成acl配置文件
@shared_task()
def generate_aclViewConf():
    aclViewdata = t_bindservice_aclView.objects.all().values()
    acl_conf_list = []
    # 遍历数据库每条记录
    for aclViewdataIns in aclViewdata:
        # 取每条记录的字段、形成数组、追加到配置list
        aclDataDict = {}
        aclDataDict['acl_name'] = aclViewdataIns['acl_name']
        aclDataDict['acl_network'] = aclViewdataIns['acl_value'].split(',')
        acl_conf_list.append(aclDataDict)

    aclConf_save_path = current_dir + '/apps/bind_configManager/output_conf/acl/' + 'acl.conf'
    response = generate_conf(temp_def=acl_template, save_path=aclConf_save_path, data=acl_conf_list)
    return response
# 生成view和zone 配置文件
@shared_task()
def generate_viewZoneConf():
    viewData = t_bindservice_aclView.objects.all().values()
    viewList = []
    for viewIns in viewData:
        viewDict = {}
        view = viewIns['view_name']
        view_matchClient = viewIns['view_matchClient']
        viewDict['view_name'] = view
        viewDict['view_matchClient'] = view_matchClient
        viewList.append(viewDict)
    '''
    遍历zone表内的数据时、aclView表内的 view_name 字段被 zone表中 zone_from_view 包含时、就在view中生成改zone的配置
    aclView表 和 zone表都有view字段、生成配置需要根据每个zone使用到的view来配置；
    每个view包含的 zone、是不一样的、可以通过下面两种方式来生成配置参数（采用一种即可）：
    1、根据aclView表内的 view_name 字段、过滤搜索zone表的zone_from_view字段（包含搜索）；
    2、根据aclView表内的 view_name 字段、通过Dict包含属性、判断zone表中 zone_from_view 字段是否包含；
    '''
    # 数据库中所有的 view 配置
    viewZone_conf_list = []

    # aclView中的view
    for view in viewList:
        '''
        1、查库过滤的方式
        zoneDbData = t_bindservice_zone.objects.filter(zone_from_view__icontains=view).values()
        2、利用dict if 判断的方式、
        '''
        # 单个view 的所有配置、包含下面的zoneList
        viewConfDict = {}
        # 单个view中的 zone list、为适配jinja模版
        zoneList = []

        # 遍历单个view中zone表每条记录、格式化数据添加到zoneList
        zoneData = t_bindservice_zone.objects.all().values()
        for zoneIns in zoneData:
            zoneConfData = {}
            # 单条zone记录
            zoneFromViewList = zoneIns['zone_from_view'].split(',')
            # 当前的view中、是否存在于当前zone记录中
            if view['view_name'] in zoneFromViewList:
                zoneConfData['zone_name'] = zoneIns['zone_name']
                zoneConfData['zone_type'] = zoneIns['zone_type']
                if zoneIns['zone_type'] == 'master':
                    # 拼接 zone 的记录文件的位置
                    zoneFile = zoneIns['zone_name'] + '.' + view['view_name'] + '.' + 'conf.host'
                    zoneConfData['zone_file_path'] = bind9_record_dir + zoneFile
                elif zoneIns['zone_type'] == 'forward':
                    zoneConfData['dest_server'] = zoneIns['zone_forwarders']

            # 当前view中、是否存在zone的记录、有则追加到zoneList中
            if zoneConfData:
                zoneList.append(zoneConfData)

        # 根据zoneList判断、view是否为空、如果这个view没有zone、则不生成view配置、遍历下一个view
        if not zoneList:
            continue

        # 整合当前view中的所有数据
        viewConfDict['view_name'] = view['view_name']
        viewConfDict['view_matchClient'] = view['view_matchClient']
        viewConfDict['zone_data'] = zoneList
        # print(viewConfDict)

        # 将当前view中的所有数据追加到 viewZone_conf_list
        viewZone_conf_list.append(viewConfDict)

    viewZoneSavePath = current_dir + '/apps/bind_configManager/output_conf/viewZone/' + 'view.conf'
    response = generate_conf(temp_def=viewAndZone_template, save_path=viewZoneSavePath, data=viewZone_conf_list)
    return response
# 生成记录配置
@shared_task()
def generate_recordConf():
    '''
    以zone表中的zone_name记录为准、循环生成zone中的record记录
    :return:
    '''
    # 获取 zone 表中所有的zone、并追加到 zoneDbList
    zoneDbDataDict = t_bindservice_zone.objects.all().values('zone_name')
    viewDbDataDict = t_bindservice_aclView.objects.all().values('view_name')

    # zone list
    zoneDbList = []
    for zoneIns in zoneDbDataDict:
        zone = zoneIns['zone_name']
        zoneDbList.append(zone)
    # view list
    viewDbList = []
    for viewIns in viewDbDataDict:
        view = viewIns['view_name']
        viewDbList.append(view)


    # zoneDbList的key 在 record表 中遍历、record表中的数据
    recordFile_nameList = []
    for zoneInsDb in zoneDbList:
        for viewInsDb in viewDbList:
            # 单个zone的配置dict
            recordConfDict = {}

            # 在数据库中过滤指定zone中和指定view中、的所有record
            filterRecordDbData = t_bindservice_record.objects.filter(record_zone=zoneInsDb, record_from_view=viewInsDb).values()
            recordInsConfList = []
            # 判断搜索结果不为空
            if filterRecordDbData:
                for filterRecord in filterRecordDbData:
                    # print('按照zone和view条件过滤后的数据', filterRecord)
                    # 处理一个zone、多条记录；zone中的多record处理、一个zone中的多条record
                    recordInsConfDict = {}
                    recordInsConfDict['record_key'] = filterRecord['record_key']
                    recordInsConfDict['record_type'] = filterRecord['record_type']
                    recordInsConfDict['record_value'] = filterRecord['record_value']
                    recordInsConfDict['record_zone'] = filterRecord['record_zone']
                    recordInsConfList.append(recordInsConfDict)

                # print('单个zone里面的所有记录', recordInsConfList)

                # # 组建配置数据体
                recordConfDict['zone_name'] = zoneInsDb
                recordConfDict['zone_ttl'] = '600'
                recordConfDict['record_data'] = recordInsConfList
                # print('完整配置体', recordConfDict)

                # 生成配置文件
                if recordInsConfList:
                    # 拼接 zone的record 记录文件
                    recordFile_name = zoneInsDb + '.' + viewInsDb + '.' + 'conf.host'
                    record_confSave_path = current_dir + '/apps/bind_configManager/output_conf/hostRecord/' + recordFile_name
                    # record_confSave_path = recordFile_name
                    res_data = generate_conf(temp_def=record_template, save_path=record_confSave_path, data=recordConfDict)

                    recordFile_nameList.append(res_data)
            # else:
                # print('搜索结果为空')
    return recordFile_nameList
