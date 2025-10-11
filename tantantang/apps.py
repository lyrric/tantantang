from django.apps import AppConfig


class TantantangConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tantantang'

    def ready(self):
        # 导入监控任务模块以启动监控线程
        try:
            import tantantang.monitor_task
        except ImportError:
            pass