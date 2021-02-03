# -*- encoding: utf-8 -*-
# File    : permissions.py
# Time    : 2021/2/1 下午5:22
# Author  : ops

from rest_framework.permissions import BasePermission

USER_GROUP_LABELS = (
    ("1", "运维组"),
)


# 权限这里、我从SSO远程获取到USER INFO后、取INFO里面的小组字段、以组为维度、控制权限
class OpsPermissions(BasePermission):
    """权限管理"""
    message = "只有OPS才能访问"

    def get_permission_from_group(cls, request):
        try:
            print('权限校验', request.user, request.auth)
            group = request.auth.get("groupName")
            return group
        except AttributeError:
            return None

    def has_permission(self, request, view):
        perms = self.get_permission_from_group(request)
        if perms:
            if perms == '运维组':
                return True
