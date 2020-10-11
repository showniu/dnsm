# -*- coding: utf-8 -*
# 创建日期： 2020-10-03 20:40 
# 文件名：generate_config.py
import django
django.setup()
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')

from jinja2 import PackageLoader, Environment
from apps.bind_service.models import t_bindservice_aclView, t_bindservice_zone, t_bindservice_record
env = Environment(loader=PackageLoader('conf_template'))
acl_template = env.get_template("acl_template.conf")
viewAndZone_template = env.get_template("viewAndZone_template.conf")
record_template = env.get_template("record_template.conf")

data = t_bindservice_record.objects.all()
print(data)

## acl template data example
# data = []
# data_i00 = {
#     "acl_name": "test001",
#     "acl_network": ["1.1.1.0/24", "1.1.1.0/24"]
# }
# data.append(data_i00)

## view template data example
# data = {
#     "view_name": "test01",
#     "acl_name": "test01",
#     "zone_data": [
#         {
#             "zone_name": 'zpidc.com',
#             "zone_type": 'master',
#             "zone_file_path": 'zone_file'
#         },
#         {
#             "zone_name": 'xx2.com',
#             "zone_type": 'forward',
#             "dest_server": '1.1.1.1'
#         }
#     ]
# }

## record template data example
# data = {
#     "zone_name": 'zpidc.com',
#     "zone_ttl": '600',
#     "record_data": [
#         {
#             "record_key": 'test001',
#             "record_value": '1.1.1.1',
#             "record_type": 'A'
#         },
#         {
#             "record_key": 'test001',
#             "record_value": 'ljp.xx.com',
#             "record_type": 'CNAME'
#         }
#     ]
#
# }


# content = record_template.render(datas=data)
# with open('./conf_output/record.conf', 'w') as f:
#     f.write(content)

