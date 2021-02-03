> 参考文档：
>
> https://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#first-steps
>
> 第一步：https://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#django-first-steps

1、启动 Borker 消息中间件
```docker run -d -p 6379:6379 redis```

2、安装celery

```pip install celery```

3、配置

一、项目根目录、/proj/proj/celery.py

`app.autodiscover_tasks()` 可以在每个Django的App中的task.py模块中自动发现所定义的任务；

```
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')

app = Celery('dnsm')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request!r}')

```

二、项目根目录、/proj/proj/__init__.py

加入以下内容、确认Django在启动时加载Celery模块。否则后面无法使用 @shared_task 装饰器

```
from .celery import app as celery_app
__all__ = ('celery_app',)

```


三、Django项目配置文件、/proj/settings/settings.xx

在前面第一个步骤、我们定义了django的settings模块作为celery的配置源、并且指定了Celery的配置前缀、所有的Celery配置都必须时大写、并且以`CELERY_`开头；

```
CELERY_TIMEZONE = "Australia/Tasmania"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_RESULT_SERIALIZER = 'json'
CELERY_BROKER_URL = 'redis://10.2.0.62:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
```
4、定义任务、/proj/app/task.py
使用 `@shared_task` 装饰器定一个任务、这里有段说明：

当前所定义的任务可能会被应用于可重用的程序中、但是可重用程序不能依赖项目本身；所以不能直接导入应用程序；

使用`@shared_task` 可以直接创建任务而不需要任何具体的应用程序

```
from celery import shared_task
@shared_task
def add(x, y):
    return x + y
```
5、在view中调用该任务

```
from app.task import add
add.delay('1', '3')
```
6、启动Celery 工作节点

`celery -A dnsm worker -l INFO`
```
celery@lijpMac-mini.local v4.3.1 (rhubarb)

Darwin-19.4.0-x86_64-i386-64bit 2020-11-16 16:41:58

[config]
.> app:         dnsm:0x109942828
.> transport:   redis://10.2.0.62:6379/0
.> results:     redis://127.0.0.1:6379/1
.> concurrency: 4 (prefork)
.> task events: OFF (enable -E to monitor tasks in this worker)

[queues]
.> celery           exchange=celery(direct) key=celery


[tasks]
  . bind_server.task.opsServerInit
  . dnsm.celery.debug_task

[2020-11-16 16:41:59,130: INFO/MainProcess] Connected to redis://10.2.0.62:6379/0
[2020-11-16 16:41:59,158: INFO/MainProcess] mingle: searching for neighbors
[2020-11-16 16:42:00,242: INFO/MainProcess] mingle: all alone
...

```
