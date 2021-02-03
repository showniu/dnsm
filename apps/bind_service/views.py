from django.shortcuts import render

from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import *
from .serializers import *
import json
from django.http import HttpResponse, JsonResponse, Http404
from rest_framework.filters import SearchFilter
from bind_ssoauth.zpsso_auth import zpSsoTokenAuthentication
from bind_ssoauth.permissions import OpsPermissions
from auditlog.models import LogEntry

# Create your views here.
class BindAclViewList(APIView):
    def get(self, *args, **kwargs):
        db_bindserver_data = t_bindservice_aclView.objects.order_by()
        serializer_data = BindAclViewSerializer(db_bindserver_data, many=True)
        res_data = serializer_data.data

        res_body = {}
        res_body['data'] = res_data
        return Response(res_body)

    def post(self, request):
        commit_data = request.data
        new_aclValue = commit_data['acl_value'].replace('\n', ',').replace('\r', ',')
        commit_data['acl_name'] = commit_data['view_name']
        commit_data['view_matchClient'] = commit_data['view_name']
        commit_data['acl_value'] = new_aclValue

        params_data = BindAclViewSerializer(data=commit_data)
        if params_data.is_valid():
            params_data.save()
            return Response(params_data.data, status=status.HTTP_201_CREATED)
        return Response(params_data.errors, status=status.HTTP_400_BAD_REQUEST)

class BindZonelist(APIView):
    def get(self, *args,  **kwargs):
        db_bindserver_data = t_bindservice_zone.objects.all()
        serializer_data = BindZoneSerializer(db_bindserver_data, many=True)

        res_data = serializer_data.data
        res_body = {}
        res_body['data'] = res_data

        return Response(res_body)

    def post(self, request):
        post_data = request.data
        print(post_data)
        if not (post_data['zone_from_view'] and post_data['zone_type'] and post_data['zone_name']):
            return Response('参数不全', status=status.HTTP_400_BAD_REQUEST)

        new_view_name = ','.join(post_data['zone_from_view'])
        post_data['zone_from_view'] = new_view_name

        zone_params_data = BindZoneSerializer(data=post_data)

        # 入库 zone 数据 （必须先入库zone 数据、否则record 配置无法生成）
        if zone_params_data.is_valid():
            zone_params_data.save()

        # 准备zone添加默认的record参数、这个zone的默认解析地址、比如定义 *.xx.com 的默认地址是 1.1.1.1
        defaultRecordDict = {}
        defaultRecordDict['record_from_view'] = post_data['zone_from_view'].split(',')
        defaultRecordDict['record_key'] = '*'
        defaultRecordDict['record_zone'] = post_data['zone_name']
        defaultRecordDict['record_type'] = 'A'
        defaultRecordDict['record_remarks'] = '添加域名时、系统自动添加默认主机记录'

        # 判断是否是master、不是master不需要创建record记录文件
        if post_data['zone_type'] == 'master':
            defaultRecordDict['record_value'] = post_data['default_value']
            opsRecord = BindRecordSearch().post(request=defaultRecordDict, ops='true')
            print(opsRecord)

        return Response(zone_params_data.data, status=status.HTTP_201_CREATED)

class BindRecordlist(APIView):
    def get(self, *args, **kwargs):
        db_bindRecord_data = t_bindservice_record.objects.all()
        serializer_data = BindRecordSerializer(db_bindRecord_data, many=True)

        res_data = serializer_data.data
        res_body = {}
        res_body['data'] = res_data

        return Response(res_body)

    def post(self, request):
        params_data = BindRecordSerializer(data=request.data)

        if params_data.is_valid():
            params_data.save()
            return Response(params_data.data, status=status.HTTP_201_CREATED)
        return Response(params_data.errors, status=status.HTTP_400_BAD_REQUEST)

class BindRecordSearch(generics.ListCreateAPIView):
    search_fields = ["record_key", "record_value"]
    filter_backends = [SearchFilter, ]
    queryset = t_bindservice_record.objects.all()
    serializer_class = BindRecordSerializer

    # 重写post 访方法
    def post(self, request, ops=None, **kwargs):
        if ops == 'true':
            post_data = request
            print(post_data)
        else:
            post_data = request.data
            print(post_data)

        # print('修改前传入参数', type(post_data), post_data)
        if not (post_data['record_key'] and post_data['record_type'] and post_data['record_value'] and post_data['record_zone'] and post_data['record_from_view']):
            return Response('参数不全', status=status.HTTP_400_BAD_REQUEST)

        paramsRecordList = post_data['record_from_view']
        # print('传入的view参数', type(paramsRecordList), paramsRecordList)
        for record_from_view_item in paramsRecordList:
            post_data['record_from_view'] = record_from_view_item
            # print('修改后的参数', type(post_data), post_data)

            params_data = BindRecordSerializer(data=post_data)
            # print('序列化数据库', params_data)

            if params_data.is_valid():
                params_data.save()

        return Response('在 %s 中添加了 %s 记录' % (paramsRecordList, post_data['record_key']), status=status.HTTP_201_CREATED)
        # return Response(params_data.errors, status=status.HTTP_400_BAD_REQUEST)

class BindAclViewOps(APIView):
    def get_object(self, obj_id):
        try:
            return t_bindservice_aclView.objects.get(id=obj_id)
        except t_bindservice_aclView.DoesNotExist:
            raise Http404
    # 对象详情
    def get(self, request, obj_id, format=None):
        res_data = self.get_object(obj_id)

        serializer_data = BindAclViewSerializer(res_data)

        return Response(serializer_data.data)

    # 删除对象
    def delete(self, request, obj_id, format=None):
        res_data = self.get_object(obj_id)
        res_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # 更新、修改数据
    def patch(self, request, obj_id):
        res_data = self.get_object(obj_id)
        serializer_data = BindAclViewSerializer(res_data, request.data, partial=True)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

class BindZoneOps(APIView):
    def get_object(self, obj_id):
        print(obj_id)
        try:
            return t_bindservice_zone.objects.get(id=obj_id)
        except t_bindservice_zone.DoesNotExist:
            raise Http404

    # 对象详情
    def get(self, request, obj_id, format=None):
        res_data = self.get_object(obj_id)

        serializer_data = BindZoneSerializer(res_data)

        return Response(serializer_data.data)

    # 删除对象
    def delete(self, request, obj_id, format=None):
        res_data = self.get_object(obj_id)
        res_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # 更新、修改数据
    def patch(self, request, obj_id):
        res_data = self.get_object(obj_id)
        serializer_data = BindZoneSerializer(res_data, request.data, partial=True)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

class BindRecordOps(APIView):
    def get_object(self, obj_id):
        try:
            return t_bindservice_record.objects.get(id=obj_id)
        except t_bindservice_record.DoesNotExist:
            raise Http404
    # 对象详情
    def get(self, request, obj_id, format=None):
        res_data = self.get_object(obj_id)

        serializer_data = BindRecordSerializer(res_data)

        return Response(serializer_data.data)
    # 删除对象
    def delete(self, request, obj_id, format=None):
        res_data = self.get_object(obj_id)
        res_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # 更新、修改数据
    def patch(self, request, obj_id):
        res_data = self.get_object(obj_id)
        serializer_data = BindRecordSerializer(res_data, request.data, partial=True)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)
