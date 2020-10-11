from django.db import models

# Create your models here.

class t_bindservice_aclView(models.Model):
    acl_name = models.CharField(max_length=512, verbose_name="同线路名", unique=True)
    acl_value = models.TextField(max_length=1024, verbose_name="线路范围", unique=True)
    view_name = models.CharField(max_length=512, verbose_name="线路名", null=False, blank=False)
    view_matchClient = models.CharField(max_length=512, verbose_name="同线路名", null=False, blank=False)
    class Meta:
        db_table = 't_bindservice_aclView'

class t_bindservice_zone(models.Model):
    zone_name = models.CharField(max_length=512, verbose_name="域名", null=True, blank=True)
    zone_type = models.CharField(max_length=512, verbose_name="域类型", null=True, blank=True)
    zone_file = models.CharField(max_length=512, verbose_name="域名记录文件", null=True, blank=True, default='')
    zone_forwarders = models.CharField(max_length=512, verbose_name="域名转发目标", null=True, blank=True, default='')
    zone_from_view = models.CharField(max_length=512, verbose_name="域名所在线路", null=True, blank=True)
    # zonf_from_view = models.ManyToManyField(t_bindservice_aclView)

    class Meta:
        db_table = 't_bindservice_zone'

class t_bindservice_record(models.Model):
    record_key = models.CharField(max_length=512, verbose_name="记录", null=True, blank=True)
    record_type = models.CharField(max_length=512, verbose_name="记录类型", null=True, blank=True)
    record_value = models.CharField(max_length=512, verbose_name="记录值", null=True, blank=True)
    record_zone = models.CharField(max_length=512, verbose_name="记录所在域", null=True, blank=True)
    record_remarks = models.CharField(max_length=512, verbose_name="备注", null=True, blank=True)
    class Meta:
        db_table = 't_bindservice_record'