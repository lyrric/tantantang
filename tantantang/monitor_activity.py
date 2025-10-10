import tantantang.logging_config
from tantantang.models import MonitorActivity
from tantantang.ttt_http import get_activity_list
from tantantang.user_config_service import get_user_config_by_uid

log = tantantang.logging_config.get_logger(__name__)


async def monitor_one(monitor_activity: MonitorActivity):
    """
    监控type为1的信息
    :param monitor_activity:
    :return:
    """
    user_config = get_user_config_by_uid(monitor_activity.user_id)
    activities = await get_activity_list(1, 10, user_config.city, user_config.lon, user_config.lat,
                                         title=monitor_activity.shop_name)
    if len(activities) < 1:
        log.info(f"No activity with shop_name:{monitor_activity.shop_name}")
        return
    