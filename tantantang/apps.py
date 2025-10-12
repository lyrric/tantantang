from django.apps import AppConfig
from tantantang.monitor_task import start_task


class TantantangConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tantantang'

    def ready(self):
        # 导入监控任务模块以启动监控线程
        try:
            start_task()
        except ImportError:
            pass
