from rest_framework.views import APIView
from rest_framework.response import Response
from bind_server.models import t_bindserver
from .setializers import BindConfTagSerializer
from .models import t_bindconf_tag
import json
import ast
from bind_server.models import t_bindserver
from bind_server.serializers import BindServerSerializer
from bind_configManager.sync_gitlab import build_conf, clone_pull_gitlab, move_conf, push_gitlab, get_project_tags
from bind_configManager.sync_bindServer import git_get_config, sync_bindConfig
from celery import chain



# 查询可以同步配置文件的服务器IP
# db_server_list = t_bindserver.objects.filter(plat_server_init='2').values_list('plat_server_ip', flat=True)

# 配置文件生成接口
class BindConfigGenerateOps(APIView):
    def post(self, request):
        '''
        生成配置文件、并将配置文件上传到gitlab
        :param request: None
        :return: clery task ID
        '''

        tasks = chain(build_conf.si(), clone_pull_gitlab.si(), move_conf.si(), push_gitlab.si(), get_project_tags.si())
        res = tasks.delay()

        return Response(res.get(), status=200)

        '''
        if ops == 'true':
            params_data = request
        else:
            params_data = request.data

        config_type = params_data['config_type']

        if config_type == 'acl':
            generate_aclViewConf()
            res_text = 'acl配置文件已经生成成功'

            return Response(res_text)
        elif config_type == 'viewZone':
            generate_viewZoneConf()
            res_text = '区域和域名配置文件已经生成成功'

            return Response(res_text)
        elif config_type == 'record':
            res_data = generate_recordConf()
            res_text = '记录配置文件已经生成成功'
            response_data = {}
            response_data['des'] = res_text
            response_data['files'] = res_data

            return Response(response_data)
        elif config_type == 'all':
            acl = generate_aclViewConf()
            viewZone = generate_viewZoneConf()
            record = generate_recordConf()
            res_text = '所有的配置文件已经生成功'


            response_data = {}
            response_data['res_text'] = res_text
            response_data['acl'] = acl
            response_data['viewZone'] = viewZone
            response_data['record'] = record
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            res_text = "请提供config_type参数、acl、viewZone、record三个选项"

            return Response(res_text)
        '''

# 配置同步到服务器作接口
class BindConfigSyncOps(APIView):
    # tag 展示
    def get(self, *args, **kwargs):
        # db_bindserver_data = t_bindserver.objects.all()
        # serializer_data = BindServerSerializer(db_bindserver_data, many=True)

        db_bindconf_data = t_bindconf_tag.objects.all().order_by('-tag_name')
        serializer_data = BindConfTagSerializer(db_bindconf_data, many=True)

        res_data = serializer_data.data
        # res_body = {}
        # res_body['data'] = res_data

        return Response(res_data)

    # 配置文件同步
    def post(self, request):
        params_data = request.data
        tag_id = params_data['tag_id']
        tag_name = params_data['tag_name']
        # servers_list = params_data['servers']

        # 先不考虑后端逻辑限制的问题、直接提供接口、参数准确就操作
        # db_tag_conf = t_bindconf_tag.objects.filter(tag_name=tag).values_list('tag_currentstatus', flat=True)
        # print(db_tag_conf)
        tag_data = t_bindconf_tag.objects.filter(id=tag_id).values('tag_related_server', 'tag_currentstatus')

        tag_related_server = tag_data[0]['tag_related_server']
        tag_currentstatus = tag_data[0]['tag_currentstatus']



        # 判断当前tag的部署状态
        res_list = []
        if tag_currentstatus:
            # 格式话当前数据
            cus_dict = {}
            for cus in ast.literal_eval(tag_currentstatus):
                ip = cus['info'].split(':')[0]
                stat = cus['info'].split(':')[1]
                cus_dict[ip] = stat

            op_serverDict = {}
            yes_opServer = []
            no_opServer = []
            for server in ast.literal_eval(tag_related_server):
                if server in cus_dict and cus_dict[server] == '部署失败':
                    # print(server + '存在于当前状态表并部署状态为失败、执行部署')
                    yes_opServer.append(server)
                elif server not in cus_dict:
                    # print(server + '不存在当前状态表、执行部署')
                    yes_opServer.append(server)
                else:
                    no_opServer.append(server)
                    # print('选择的服务器和已经部署的服务器完全相同、本次不部署')
                op_serverDict['yes'] = yes_opServer
                op_serverDict['no'] = no_opServer

            print('执行的服务器', yes_opServer)
            print('不执行的服务器', no_opServer)

            # 需要执行的服务器、只有参数中服务器才会继续有需要执行的
            if op_serverDict['yes']:
                for ser in op_serverDict['yes']:
                    res_dict = {}
                    res_dict['type'] = 'info'
                    res_dict['info'] = ser + ':' + '执行中...'
                    res_list.append(res_dict)
                for serv in op_serverDict['no']:
                    res_dict = {}
                    res_dict['type'] = 'success'
                    res_dict['info'] = serv + ':' + '已部署'
                    res_list.append(res_dict)

                t_bindconf_tag.objects.filter(id=tag_id).update(tag_currentstatus=res_list)
                tasks = chain(git_get_config.si(tag_name), sync_bindConfig.si(op_serverDict['yes'],
                                                                              op_serverDict['no'], tag_id))
                res = tasks.delay()
                return Response(res_list, status=200)
        else:
            # 没有过部署记录
            servers_list = ast.literal_eval(tag_related_server)
            tasks = chain(git_get_config.si(tag_name), sync_bindConfig.si(opServer=servers_list,
                                                                          noOpserver=None, tag_id=tag_id))
            res = tasks.delay()

            for hostIp in servers_list:
                res_dict = {}
                res_dict['type'] = 'info'
                res_dict['info'] = hostIp + ':' + '执行中...'
                res_list.append(res_dict)
            t_bindconf_tag.objects.filter(id=tag_id).update(tag_currentstatus=res_list)

        return Response(res_list, status=200)

        # tag_data = []
        # for server in servers_list:
        #     tag_datadict = {}
        #     tag_datadict['serverIp'] = server
        #     tag_datadict['syncStatus'] = '执行中...'
        #     tag_data.append(tag_datadict)

        # t_bindconf_tag.objects.filter(tag_name=tag).update(tag_currentstatus=tag_data)


        ## tasks = chain(git_get_config.si(tag), sync_bindConfig.si(servers_list))
        # tasks = chain(git_get_config.si(tag))
        # res = tasks.delay()

        # return Response(res.get(), status=200)

        # 生成配置文件
        # genConfRes = BindConfigGenerateOps().post(request=generateConfig_reqParams, ops='true')
        # genConfResBody = genConfRes.data
        #
        # aclConfFile = genConfResBody['acl']
        # viewZoneConfFile = genConfResBody['viewZone']
        # recordConfFile = genConfResBody['record']

        # res = chain(genConfResBody)

        # if aclConfFile and viewZoneConfFile and  recordConfFile:
        #     sync_re = sync_gitlab.sync_main()

        '''目标服务器远程目录（直接同步到服务器的方式、弃用）
        bind9_basicConfig_dir = '/usr/local/bind9/etc/'
        bind9_acl_dir = bind9_basicConfig_dir + 'acl/'
        bind9_viewZone_dir = bind9_basicConfig_dir + 'viewZone/'
        bind9_record_dir = bind9_basicConfig_dir + 'hostRecord/'
        # path转list取目录
        recordConfFileDir = recordConfFile[0].split('/')[0:-1]
        recordConfFileDir = "/".join(recordConfFileDir)

        #
        res = []
        for server in server_list:
            aclConfOps_log = sync_OpsBindConfig.delay(server=server, src=aclConfFile, dest=bind9_acl_dir)
            viewZoneOps_log = sync_OpsBindConfig.delay(server=server, src=viewZoneConfFile, dest=bind9_viewZone_dir)
            recordOPs_log = sync_OpsBindConfig.delay(server=server, src=recordConfFileDir, dest=bind9_record_dir, record = 'true')

            ops_log = {}
            ops_log['acllog'] = aclConfOps_log
            ops_log['viewzonelog'] = viewZoneOps_log
            ops_log['recordlog'] = recordOPs_log
            res.append(ops_log)
        # print('uuu', ops_log)

        #


        
        '''

# Gitlab TAG 标签 与服务器关联
class BindConfTagRelated(APIView):
    def post(self, request):
        params_data = request.data
        tag_id = params_data['tag_id']
        server_list = params_data['servers']

        t_bindconf_tag.objects.filter(id=tag_id).update(tag_related_server=server_list)
        print('传入的服务器', server_list)
        return Response(server_list, status=200)
