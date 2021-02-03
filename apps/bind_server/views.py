from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import t_bindserver
from .serializers import BindServerSerializer, BindServerIpSerializer
from bind_server.task import opsServerInit
from django.http import HttpResponse, JsonResponse, Http404
from operation_log.models import t_deleteddata_server, t_deleteddata_aclview, t_deleteddata_zone, t_deleteddata_record
from rest_framework.filters import SearchFilter
from rest_framework import generics
from rest_framework import serializers

import os

# bind server list 、新增服务器
class BindServerListView(generics.ListCreateAPIView):
    search_fields = ["plat_server_ip"]
    filter_backends = [SearchFilter, ]
    queryset = t_bindserver.objects.all()
    serializer_class = BindServerSerializer
    ''' 旧代码
    def get(self, request, *args, **kwargs):
        # db_bindserver_data = t_bindserver.objects.all()
        # serializer_data = BindServerSerializer(db_bindserver_data, many=True)
        #
        # res_data = serializer_data.data
        # res_body = {}
        # res_body['data'] = res_data
        #
        # return Response(res_body)

    def post(self, request, **kwargs):
        params_data = BindServerSerializer(data=request.data)

        if params_data.is_valid():
            params_data.save()
            return Response(params_data.data, status=status.HTTP_201_CREATED)
        return Response(params_data.errors, status=status.HTTP_400_BAD_REQUEST)

        # post body
        # {
        #     "plat_server_hostname": "test-host01",
        #     "plat_server_ip": "1.1.1.1",
        #     "plat_server_port": "22",
        #     "plat_server_nopass": "yes",
        #     "plat_server_role": "master"
        # }
    '''

class BindServerIPListView(APIView):
    def get(self, request, *args, **kwargs):
        # queryset = t_bindserver.objects.values_list('plat_server_ip', flat=True)
        queryset = t_bindserver.objects.all()
        server_serializer = BindServerIpSerializer(queryset, many=True)
        # print('server_serializer', server_serializer)
        server_data = server_serializer.data
        # print('server_data', server_data)
        return Response(server_data)

# 操作服务器、get、delete
class BindServerOpsView(APIView):
    def get_object(self, obj_id):
        print(obj_id)
        try:
            return t_bindserver.objects.get(id=obj_id)
        except t_bindserver.DoesNotExist:
            raise Http404

    # 对象详情
    def get(self, request, obj_id, format=None):
        res_data = self.get_object(obj_id)

        serializer_data = BindServerSerializer(res_data)

        return Response(serializer_data.data)

    def delete(self, request, obj_id, format=None):
        res_data = self.get_object(obj_id)
        serializer_data = (BindServerSerializer(res_data)).data
        his_id = serializer_data['id']
        # 保存即将删除的数据到 t_deletedata 表
        t_deleteddata_server.objects.create(his_id=his_id, msg=serializer_data)

        res_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 初始化服务器（安装bindserver）
class BindServerInit(APIView):
    # 根据ID查询数据
    def get_object(self, obj_id):
        try:
            return t_bindserver.objects.get(id=obj_id)
        except t_bindserver.DoesNotExist:
            raise Http404

    # 根据IP查询数据、
    def get_object_for_ip(self, obj_ip):
        try:
            return t_bindserver.objects.get(plat_server_ip=obj_ip)
        except t_bindserver.DoesNotExist:
            return obj_ip + ' 在数据库中不存在！'

    def post(self, request):
        servers = request.data
        # 结果list
        resList = []

        # 处理单个server或多个server
        for host in servers[::-1]:
            mdData = {}
            # 修改server状态为1、"初始化中"
            mdData['plat_server_init'] = '1'
            resData = self.get_object_for_ip(host)

            # 验证IP参数是否存在数据库中、如果数据不存在、则返回的是str
            if isinstance(resData, str):
                # 删除list中、数据库里查询不到的服务器
                servers.remove(host)
                non_existent = {}
                non_existent[host] = '数据库中不存在这条服务器记录'
                resList.append(non_existent)
            # 数据库中存在
            else:
                serverDbdata = BindServerSerializer(resData)
                # 判断这台服务器的当前状态
                initState = serverDbdata['plat_server_init'].value
                if initState == None or initState == '0':
                    c = BindServerSerializer(resData, mdData, partial=True)
                    if c.is_valid():
                        c.save()
                        resList.append(c.data)
                elif initState == '1':
                    alreadyIng = {}
                    alreadyIng[host] = '服务器正在初始化中...'
                    resList.append(alreadyIng)
                    # 删除有状态的服务器
                    servers.remove(host)
                elif initState == '2':
                    alreadyIng = {}
                    alreadyIng[host] = '服务器已经初始化过！'
                    resList.append(alreadyIng)
                    # 删除有状态的服务器
                    servers.remove(host)
                elif initState == '3':
                    alreadyIng = {}
                    alreadyIng[host] = '服务器已经初始失败、主机不存在或者无法正常登录！'
                    resList.append(alreadyIng)
                    # 删除有状态的服务器
                    servers.remove(host)
                else:
                    alreadyIng = {}
                    alreadyIng[host] = '未知问题.'
                    resList.append(alreadyIng)
                    # 删除有状态的服务器
                    servers.remove(host)

        # 扔到后台、异步处理
        if servers:
            opsServerInit.delay(servers)
            # opsServerInit(servers)
        else:
            pass

        return Response(servers)

# 重置服务器状态
class ResetBindServerInit(APIView):
    # 根据ID查询数据
    def get_object(self, obj_id):
        try:
            return t_bindserver.objects.get(id=obj_id)
        except t_bindserver.DoesNotExist:
            raise Http404

    # 重置服务器状态
    def patch(self, request, obj_id):
        res_data = self.get_object(obj_id)
        update_data = {}
        update_data['plat_server_init'] = '0'
        serializer_data = BindServerSerializer(res_data, update_data, partial=True)

        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        return Response('更新失败', status=status.HTTP_404_NOT_FOUND)
