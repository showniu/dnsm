from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(t_bindservice_aclView)
admin.site.register(t_bindservice_zone)
admin.site.register(t_bindservice_record)
