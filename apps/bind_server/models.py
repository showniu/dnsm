from django.db import models
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField

# Create your models here.

class t_bindserver(models.Model):
    plat_server_createtime = models.DateField(auto_now_add=True, verbose_name="修改时间", null=True, blank=True)
    plat_server_hostname = models.CharField(max_length=512, verbose_name="平台主机名", null=True, blank=True)
    plat_server_ip = models.CharField(max_length=512, verbose_name="平台主机IP", null=True, blank=True)
    plat_server_init = models.CharField(max_length=512, verbose_name="服务器是否初始化", null=True, blank=True)
    plat_server_port = models.CharField(max_length=128, verbose_name="平台主机通信端口", null=True, blank=True)
    plat_server_nopass = models.CharField(max_length=128, verbose_name="是否支持免密登录", null=True, blank=True)
    plat_server_role = models.CharField(max_length=128,  verbose_name="平台主机角色", null=True, blank=True)
    # plat_server_history = AuditlogHistoryField()

    class Meta:
        db_table = 't_bindserver'



auditlog.register(t_bindserver)


'''
plat_server_init: 0 or 1 or 2 or 3
0: 未初始化
1: 初始化中
2: 已初始化
3: 初始化失败
'''
