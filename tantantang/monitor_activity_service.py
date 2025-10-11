import json
import time
from typing import List

from django_redis import get_redis_connection

from tantantang.models import MonitorActivity


def _monitor_activity_key():
    """获取MonitorActivity在Redis中存储的hash key"""
    return "TTT:MONITOR_ACTIVITIES"


def add_monitor_activity(monitor_activity: MonitorActivity):
    """
    添加监控活动到Redis hash
    :param monitor_activity: MonitorActivity实例
    """
    conn = get_redis_connection()
    key = _monitor_activity_key()
    monitor_activity.m_id = int(time.time() * 1000)

    # 将MonitorActivity对象转换为字典，再序列化为JSON字符串
    monitor_activity_dict = monitor_activity.to_dict()
    monitor_activity_json = json.dumps(monitor_activity_dict)

    # 在hash中存储监控活动详情，使用m_id作为field
    conn.hset(key, monitor_activity.m_id, monitor_activity_json)

    return monitor_activity.m_id


def get_all_monitor_activities() -> List[MonitorActivity]:
    """
    获取所有监控活动
    :return: MonitorActivity对象列表
    """
    conn = get_redis_connection()
    key = _monitor_activity_key()

    # 获取所有监控活动
    monitor_activities_dict = conn.hgetall(key)

    monitor_activities: List[MonitorActivity] = []
    for m_id, monitor_activity_json in monitor_activities_dict.items():
        # 将JSON字符串转换为字典
        monitor_activity_dict = json.loads(monitor_activity_json)
        # 创建MonitorActivity对象
        monitor_activity = MonitorActivity.from_dict(monitor_activity_dict)
        monitor_activities.append(monitor_activity)

    return monitor_activities


def get_monitor_activity_by_id(m_id: int):
    """
    根据m_id获取监控活动
    :param m_id: 监控活动m_id
    :return: MonitorActivity对象或None
    """
    conn = get_redis_connection()
    key = _monitor_activity_key()

    monitor_activity_json = conn.hget(key, m_id)
    if monitor_activity_json:
        # 将JSON字符串转换为字典
        monitor_activity_dict = json.loads(monitor_activity_json)
        # 创建MonitorActivity对象
        monitor_activity = MonitorActivity.from_dict(monitor_activity_dict)
        return monitor_activity
    return None


def update_monitor_activity_by_id(updated_monitor_activity: MonitorActivity):
    """
    根据m_id更新监控活动
    :param updated_monitor_activity: 新的MonitorActivity实例
    :return: bool 是否更新成功
    """
    # 先检查监控活动是否存在
    existing_activity = get_monitor_activity_by_id(updated_monitor_activity.m_id)
    if not existing_activity:
        return False

    conn = get_redis_connection()
    key = _monitor_activity_key()
    existing_activity.threshold_price = updated_monitor_activity.threshold_price
    existing_activity.status = updated_monitor_activity.status
    # 更新监控活动
    updated_dict = existing_activity.to_dict()
    updated_json = json.dumps(updated_dict)
    conn.hset(key, existing_activity.m_id, updated_json)
    return True


def delete_monitor_activity_by_id(m_id: int):
    """
    根据m_id删除监控活动
    :param m_id: 要删除的监控活动m_id
    :return: bool 是否删除成功
    """
    conn = get_redis_connection()
    key = _monitor_activity_key()

    # 删除hash中的数据
    result = conn.hdel(key, m_id)

    # 返回是否删除成功
    return result > 0
