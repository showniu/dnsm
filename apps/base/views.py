import logging
import datetime
from django.shortcuts import render
from rest_framework_jwt.views import VerifyJSONWebToken
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings
import requests

logger = logging.getLogger(__name__)


class DoInfoAPIView(VerifyJSONWebToken):
    def get(self, request, *args, **kwargs):
        try:
            authorization = request.META.get(settings.HTTP_AUTHORIZATION).split()[-1]
            headers = {
                "authorization": "Bearer " + authorization
            }
            resp = requests.get(url=settings.AUTH_URL, headers=headers)
            print(resp.json())
            if resp.status_code == 200:
                return Response(data=resp.json())
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except (AttributeError, IndexError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
