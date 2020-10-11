from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import t_bindserver
from .serializers import BindServerSerializer

from django.http import HttpResponse, JsonResponse, Http404

# bind server list 、新增
class BindServerListView(APIView):
    def get(self, *args, **kwargs):
        db_bindserver_data = t_bindserver.objects.all()
        serializer_data = BindServerSerializer(db_bindserver_data, many=True)

        res_data = serializer_data.data
        res_body = {}
        res_body['data'] = res_data

        return Response(res_body)

    def post(self, request):
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
        res_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
