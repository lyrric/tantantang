import datetime
import tantantang.logging_config

log = tantantang.logging_config.get_logger(__name__)


def start():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"开始执行于: {current_time}")
