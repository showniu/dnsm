import requests
from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from rest_framework.response import Response


class User:
    def __init__(self, data=None):
        self.data = data

    @property
    def is_authenticated(self):
        return bool(self.id)


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            authorization = self.try_get_cookies(request)
            if not authorization:
                authorization = request.META.get(settings.HTTP_AUTHORIZATION).split()[-1]

            headers = {
                "authorization": "Bearer " + authorization
            }
            resp = requests.get(url=settings.AUTH_URL, headers=headers)
            if resp.status_code != 200:
                return Response(status=resp.status_code, data=resp.json())
            user = User(data=resp.json())
            for key, value in resp.json().items():
                setattr(user, key, value)
            return user, None
        except (IndexError, AttributeError):
            return None, None

    def try_get_cookies(self, request):
        return request.COOKIES.get("INNER_AUTHENTICATION")
