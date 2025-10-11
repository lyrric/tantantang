import asyncio
import json
import time
import threading
from datetime import datetime

from django_redis import get_redis_connection

import tantantang.logging_config
from tantantang.models import MonitorActivity, Activity
from tantantang.ttt_http import get_activity_list
from tantantang.user_config_service import get_user_config_by_uid
from tantantang.message import send_message
from tantantang.monitor_activity_service import get_all_monitor_activities

log = tantantang.logging_config.get_logger(__name__)

OLD_ACTIVITY_PRE_FIX = "TTT:OLD_ACTIVITY:"


def start_monitor():
    while True:
        # 检查当前时间是否在00:00到08:00之间，如果是则跳过执行
        current_hour = datetime.now().hour
        if 0 <= current_hour < 8:
            log.info(f"当前时间为 {current_hour} 点，处于00:00-08:00时间段，跳过执行监控任务")
            time.sleep(60)
            continue

        monitors = get_all_monitor_activities()
        tasks = []
        for monitor in monitors:
            if monitor.status != 1:
                continue
            # 创建协程任务而不是直接创建asyncio任务
            tasks.append(monitor_one(monitor))

        # 创建新的事件循环并运行所有任务
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # 等待所有任务完成
            loop.run_until_complete(asyncio.gather(*tasks))
        finally:
            loop.close()

        time.sleep(60)


"""
  在新线程中启动监控任务
  """
thread = threading.Thread(target=start_monitor)
thread.daemon = True  # 设置为守护线程，主程序退出时该线程也会退出
thread.start()


async def monitor_one(monitor_activity: MonitorActivity):
    """
    监控type为1的信息
    :param monitor_activity:
    :return:
    """
    log.info(f"开始监控：{monitor_activity.shop_name}")
    try:
        user_config = get_user_config_by_uid(monitor_activity.user_id)
        current_activities = await get_activity_list(1, 10, user_config.city, lon=user_config.lnt, lat=user_config.lat,
                                                     title=monitor_activity.shop_name)
        if len(current_activities) < 1:
            log.info(f"{user_config.name} No activity with shop_name:{monitor_activity.shop_name}")
            return
        current_activities = [activity for activity in current_activities if
                              activity.shop_name == monitor_activity.shop_name and activity.sy_store > 0]
        if len(current_activities) < 1:
            log.info(f"{user_config.name} No activity with shop_name:{monitor_activity.shop_name}")
            return
        log.info(
            f"{user_config.name} activity count is {len(current_activities)} with shop_name:{monitor_activity.shop_name}")
        old_activity_key = f"{OLD_ACTIVITY_PRE_FIX}{monitor_activity.user_id}"
        conn = get_redis_connection()
        data = conn.hget(old_activity_key, monitor_activity.shop_name)
        old_activities = []
        if data is not None:
            dicts = json.loads(data.decode(encoding='utf-8'))
            for dict_ in dicts:
                old_activity = Activity.from_dict(json.loads(dict_))
                old_activities.append(old_activity)
        # 删除old_activities中不在current_activities中的数据（通过activitygoods_id比较）
        current_activity_ids = {activity.activitygoods_id for activity in current_activities}
        old_activities = [old_act for old_act in old_activities if old_act.activitygoods_id in current_activity_ids]
        message_str = ''
        for current_activity in current_activities:
            old_activity = [activity for activity in old_activities if
                            activity.activitygoods_id == current_activity.activitygoods_id]
            if len(old_activity) <= 0:
                # 添加新的数据
                old_activities.append(current_activity)
            if current_activity.price > monitor_activity.threshold_price:
                continue
            if len(old_activity) <= 0:
                # 新数据
                log.info(f"{user_config.name} 找到新的活动：{current_activity.title} 当前价格:{current_activity.price}")
                message_str += build_message(current_activity, None)
            elif current_activity.price != old_activity[0].price:
                # 判断价格是否有变化
                log.info(
                    f"{user_config.name} 找到新的活动：{current_activity.title} 价格:{old_activity[0].price}-->{current_activity.price}")
                message_str += build_message(current_activity, old_activity[0])
                # 将新的价格赋值给老的数据，这里做的不太好，应该讲新的数据整个替换掉老数据
                old_activity[0].price = current_activity.price
        # 保存数据
        save_data = [json.dumps(activity.to_dict()) for activity in old_activities]
        conn.hset(old_activity_key, monitor_activity.shop_name, json.dumps(save_data))
        # 发送消息
        if len(message_str) > 0:
            await send_message(user_config.spt, "有新的活动提醒了", message_str)
        log.info(f"监控完成：{monitor_activity.shop_name}")
    except Exception as e:
        log.error(f"监控异常：{monitor_activity.shop_name}")
        log.error(e, exc_info=True)


def build_message(current_activity: Activity, old_activity: Activity | None) -> str:
    message = f"标题:{current_activity.title}<br/>"
    message += f"门店:{current_activity.shop_name}<br/>"
    if old_activity is not None:
        message += f"价格:{old_activity.price}-->{current_activity.price}<br/>"
    else:
        message += f"价格:{current_activity.price}<br/>"
    message += "<br/>"
    return message
