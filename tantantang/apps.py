from django.apps import AppConfig
from django.conf import settings

from tantantang.monitor_task import start_task

import tantantang.logging_config

log = tantantang.logging_config.get_logger(__name__)


def _is_reload_check():
    """
    判断是否是Django的代码重载检查过程
    在开发环境中，Django会fork进程来检查代码变更，我们需要避免在这种情况下启动重复的任务
    """
    import os
    return os.environ.get('RUN_MAIN') == 'true'


class TantantangConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tantantang'

    def ready(self):
        # 导入监控任务模块以启动监控线程
        # 仅在非测试模式且非代码重载检查时启动监控任务
        try:
            if not settings.DEBUG or not _is_reload_check():
                start_task()
            else:
                log.info("代码重载检查，跳过启动监控任务")
        except ImportError:
            pass
