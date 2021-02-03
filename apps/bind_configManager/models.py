from django.db import models

# Create your models here.

class t_bindconf_tag(models.Model):
    tag_name = models.CharField(max_length=128,  verbose_name="TAG名", null=True, blank=True)
    tag_test = models.CharField(max_length=128,  verbose_name="TAG测试状态", null=True, blank=True)
    tag_currentstatus = models.CharField(max_length=128,  verbose_name="TAG当前状态", null=True, blank=True)
    tag_related_server = models.CharField(max_length=128,  verbose_name="TAG关联服务器", null=True, blank=True)

    class Meta:
        db_table = 't_bindconf_tag'
