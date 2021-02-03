# -*- encoding: utf-8 -*-
# File    : zpsso_auth.py.py
# Time    : 2021/1/25 下午5:17
# Author  : ops
import logging
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import BaseAuthentication
# from bind_ssoauth.models import User
logger = logging.getLogger(__name__)

class zpSsoTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        前端的认证接口 每次请求必须走这个认证 来认证user
        :param request:
        :return:
        """
        import base64
        import requests
        cookies_auth = request.META.get("HTTP_AUTHORIZATION")
        if not cookies_auth:
            return
        cookies_auth = cookies_auth.split()[-1]
        if not cookies_auth:
            return
        try:
            token = base64.decodebytes(cookies_auth.encode("utf8"))
            # SSO的地址
            url = "sso url"
            res = requests.get(url.format(token.decode("utf8")))
            data = res.json()

        except Exception as e:
            logger.warning("CommonTokenAuthentication 认证出现异常 请求其他认证 errors{}".format(e))
            return
        # print('登录认证auth', data)
        # 认证了 token
        code = data.get("code")
        # return data.get('data')['cnName']
        if code == 200:
            login_name = data.get("data").get("loginName")
            # user = User.objects.filter(username=login_name).first()
            return (login_name, data.get('data'))
