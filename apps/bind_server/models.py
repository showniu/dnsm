from django.db import models

# Create your models here.

class t_bindserver(models.Model):
    plat_server_createtime = models.DateField(auto_now_add=True, verbose_name="修改时间", null=True, blank=True)
    plat_server_hostname = models.CharField(max_length=512, verbose_name="平台主机名", null=True, blank=True)
    plat_server_ip = models.CharField(max_length=512, verbose_name="平台主机IP", null=True, blank=True)
    plat_server_port = models.CharField(max_length=128, verbose_name="平台主机通信端口", null=True, blank=True)
    plat_server_nopass = models.CharField(max_length=128, verbose_name="是否支持免密登录", null=True, blank=True)
    plat_server_role = models.CharField(max_length=128,  verbose_name="平台主机角色", null=True, blank=True)

    class Meta:
        db_table = 't_bindserver'