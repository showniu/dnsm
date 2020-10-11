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


# Create your views here.
class BindAclViewList(APIView):
    def get(self, *args, **kwargs):
        db_bindserver_data = t_bindservice_aclView.objects.order_by()
        serializer_data = BindAclViewSerializer(db_bindserver_data, many=True)
        res_data = serializer_data.data

        # 修改models返回的数据格式, acl_value str修改为list
        # for data in res_data:
        #     acl_value_str = data['acl_value']
        #     acl_value_list = acl_value_str.split()
        #     data['acl_value'] = acl_value_list

        res_body = {}
        res_body['data'] = res_data
        # print(res_data, type(res_data))
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

        if not (post_data['zone_from_view'] and post_data['zone_type'] and post_data['zone_name']):
            return Response('参数不全', status=status.HTTP_400_BAD_REQUEST)

        new_view_name = ','.join(post_data['zone_from_view'])
        post_data['zone_from_view'] = new_view_name
        params_data = BindZoneSerializer(data=post_data)

        if params_data.is_valid():
            params_data.save()
            return Response(params_data.data, status=status.HTTP_201_CREATED)
        return Response(params_data.errors, status=status.HTTP_400_BAD_REQUEST)

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
    search_fields = ["record_key", ]
    filter_backends = [SearchFilter, ]
    queryset = t_bindservice_record.objects.all()
    serializer_class = BindRecordSerializer


class BindAclViewOps(APIView):
    def get_object(self, obj_id):
        print(obj_id)
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
        print(obj_id)
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
