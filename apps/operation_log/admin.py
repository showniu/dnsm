from django.contrib import admin

# Register your models here.
from .models import t_deleteddata_server, t_deleteddata_aclview, t_deleteddata_zone , t_deleteddata_record

admin.site.register(t_deleteddata_server)
admin.site.register(t_deleteddata_aclview)
admin.site.register(t_deleteddata_record)
admin.site.register(t_deleteddata_zone)
