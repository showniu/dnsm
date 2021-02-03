from django.db import models

# Create your models here.
#
class t_deleteddata_server(models.Model):
    his_id = models.CharField(max_length=128, verbose_name="历史数据的ID", null=True, blank=True)
    msg = models.CharField(max_length=1024, verbose_name="删除的数据", null=True, blank=True)

    class Meta:
        db_table = 't_deleteddata_server'

class t_deleteddata_aclview(models.Model):
    his_id = models.CharField(max_length=128, verbose_name="历史数据的ID", null=True, blank=True)
    msg = models.CharField(max_length=1024, verbose_name="删除的数据", null=True, blank=True)

    class Meta:
        db_table = 't_deleteddata_aclview'

class t_deleteddata_zone(models.Model):
    his_id = models.CharField(max_length=128, verbose_name="历史数据的ID", null=True, blank=True)
    msg = models.CharField(max_length=1024, verbose_name="删除的数据", null=True, blank=True)

    class Meta:
        db_table = 't_deleteddata_zone'

class t_deleteddata_record(models.Model):
    his_id = models.CharField(max_length=128, verbose_name="历史数据的ID", null=True, blank=True)
    msg = models.CharField(max_length=1024, verbose_name="删除的数据", null=True, blank=True)

    class Meta:
        db_table = 't_deleteddata_record'

'''
这些表暂时没有用了、因为利用里操作记录表里面的删除记录、删除操作里面记录有项目的信息；先留着暂时不处理
'''
