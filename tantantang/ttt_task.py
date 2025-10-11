import asyncio
import datetime
import json
import queue
import time
from concurrent.futures import ThreadPoolExecutor

from django_redis import get_redis_connection

import tantantang.logging_config
from tantantang import ttt_http
from tantantang import user_config_service
from tantantang.message import send_message
from tantantang.models import UserConfig, Activity
from tantantang.ttt_http import get_city_list

thread_pool = ThreadPoolExecutor(max_workers=1)

log = tantantang.logging_config.get_logger(__name__)


async def start_one(user_config: UserConfig):
    log.info(f"开始执行自动砍价：{user_config.name}")

    update_bargain_state(user_config)
    task_executor = ThreadPoolExecutor(
        max_workers=1, thread_name_prefix="task_thread")
    task_queue: queue.Queue[Activity] = queue.Queue()
    cities = await get_city_list()
    # 对城市列表按city字段进行排序
    cities.sort(key=lambda x: x.city)
    # 检查是否需要从上次的进度继续执行
    start_city_index = 0
    start_page_num = 1
    if user_config.bar_gain_state.status in [3] and is_today(user_config.bar_gain_state.current_time):
        # 根据进度确定起始城市和页码
        for i, city in enumerate(cities):
            if city.city == user_config.bar_gain_state.city:
                start_city_index = i
                start_page_num = user_config.bar_gain_state.page_num
                break
        load_history(user_config, task_queue)
    try:
        user_config.bar_gain_state.status = 2
        update_bargain_state(user_config)
        # 直接提交同步包装方法
        task_executor.submit(sync_bargain_wrapper, task_queue, user_config)
        for city_index in range(start_city_index, len(cities)):
            city = cities[city_index]
            city_name = city.city
            user_config.bar_gain_state.city = city_name
            # 确定起始页码
            start_page = start_page_num if city_index == start_city_index else 1
            for page_num in range(start_page, 999):
                user_config.bar_gain_state.page_num = page_num
                # 任务数量大于20则暂时不生成任务
                while task_queue.qsize() > 50:
                    if is_pause(user_config):
                        do_pause(user_config, task_queue)
                        return
                    await asyncio.sleep(1)
                log.info(f"name：{user_config.name}，开始执行，城市:{city_name}，第{page_num}页")
                activities = await ttt_http.get_activity_list(page_num, 10, city_name, token=user_config.token)
                if len(activities) == 0:
                    break
                activities = [activity for activity in activities if
                              activity.kan == 0 and activity.is_cut == 2 and activity.sy_store > 0]
                for activity in activities:
                    task_queue.put_nowait(activity)
                if is_pause(user_config):
                    do_pause(user_config, task_queue)
                    return
        log.info(f"name: {user_config.name}，城市遍历完成，等待队列执行完毕")
        user_config.bar_gain_state.status = 4
        while True:
            if is_pause(user_config):
                do_pause(user_config, task_queue)
                break
            if task_queue.empty():
                # 如果刚刚最后一批
                user_config.bar_gain_state.status = 4
                update_bargain_state(user_config)
                break
    except Exception as e:
        log.error(f"name:{user_config.name}，自动砍价失败：{user_config.name}", exc_info=e)
        user_config.bar_gain_state.status = 3
        user_config.bar_gain_state.remark = str(e)
        update_bargain_state(user_config)
        await send_message(user_config.spt, "自动砍价异常",
                           f"name:{user_config.name}，砍价异常<br/> 错误信息：{e}")


def load_history(user_config: UserConfig, task_queue: queue.Queue):
    conn = get_redis_connection()
    json_data_list = conn.lpop(f'{pause_pre_fix}{user_config.user_id}', 999)
    if json_data_list is not None:
        for json_data in json_data_list:
            activity = Activity.from_dict(json.loads(json_data.decode(encoding='utf-8')))
            task_queue.put_nowait(activity)


def sync_bargain_wrapper(task_queue: queue.Queue, user_config: UserConfig):
    asyncio.run(bargain(task_queue, user_config))


async def bargain(task_queue: queue.Queue, user_config: UserConfig):
    start_time = time.time()  # 记录开始时间
    tg = 0
    count = 0
    while user_config.bar_gain_state.status != 3:
        activities = []
        for i in range(8):
            if not task_queue.empty():
                activities.append(task_queue.get())
        if len(activities) > 0:
            tasks = [asyncio.create_task(bargain_one(user_config, activity)) for activity in activities]
            results = await asyncio.gather(*tasks)
            count += len(tasks)
            tg += sum(results)
            log.info(f"name:{user_config.name}, count={count}, tg={tg}")
        else:
            # 队列为空
            if user_config.bar_gain_state.status == 4:
                ##活动遍历已完成、且队列为空，则表示已完成
                log.info(f"name: {user_config.name}, all success, count = {count}, tg={tg}")
                break
            await asyncio.sleep(1)
    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算耗时
    log.info(f"name: {user_config.name}, 砍价任务结束，总耗时: {elapsed_time:.2f}秒")
    if user_config.bar_gain_state.status == 3:
        await send_message(user_config.spt, "自动砍价异常",
                           f"name: {user_config.name}<br/>自动砍价异常<br/>原因：{user_config.bar_gain_state.remark}<br/>总次数: {count}<br/>累计获得糖果: {tg}<br/>执行时间: {elapsed_time:.2f}秒")
    else:
        await send_message(user_config.spt, "自动砍价完成",
                           f"name: {user_config.name}<br/>自动砍价完成<br/>总次数: {count}<br/>累计获得糖果: {tg}<br/>执行时间: {elapsed_time:.2f}秒")


async def bargain_one(user_config: UserConfig, activity: Activity, num: int = 1) -> int:
    """
    单个商品砍价逻辑
    返回获取的糖果数量
    :param user_config 用户配置
    :param activity 活动信息
    :param num 重试次数
    """
    http_result = await ttt_http.bar_gain(user_config.token, user_config.user_id, user_config.key,
                                          activity.activitygoods_id)
    if http_result.code == 200:
        if http_result.data == 0:
            log.warning(f"name:{user_config.name} 砍价完成，但是没有获取到糖果，应该是key过期了")
            user_config.bar_gain_state.status = 3
            user_config.bar_gain_state.remark = '砍价完成，但是没有获取到糖果，应该是key过期了'
            return 0
        else:
            log.info(
                f"name:{user_config.name}，activity_id：{activity.activity_id}, name: {activity.shop_name}，砍价完成，获得糖果:{http_result.data}")
            return http_result.data
    elif ('商品库存数不足' in http_result.msg
          or '不能再砍啦' in http_result.msg
          or '每个商品一天只能砍一次哦' in http_result.msg
    ):
        log.info(f"name:{user_config.name}，{http_result.msg}：{activity} {user_config}")
        return 0
    elif ('当前砍价人数过多，请稍后砍价' in http_result.msg
          or '出差了' in http_result.msg
          or '信号灯超时时间已到' in http_result.msg):
        log.info(f"name:{user_config.name}，{http_result.msg}，等待3s秒继续：{activity} {user_config}")
        await asyncio.sleep(1)
        num += 1
        if num > 5:
            return 0
        return await bargain_one(user_config, activity, num)
    else:
        log.error(f"name:{user_config.name}，砍价失败：{activity} {http_result.msg}")
        if user_config.bar_gain_state.status == 4:
            # 城市活动遍历都已经完成了，剩下的活动砍价出错，这里就直接忽略
            pass
        else:
            user_config.bar_gain_state.status = 3
            user_config.bar_gain_state.remark = http_result.msg
        return 0


def is_pause(user_config: UserConfig) -> bool:
    """
    判断是否有砍价出现未知异常，出现异常则需要暂停工作
    """
    return user_config.bar_gain_state.status == 3


pause_pre_fix = "ttt:pause:"


def do_pause(user_config: UserConfig, task_queue: queue.Queue[Activity]):
    ##保存当前状态
    log.info(f"name:{user_config.name} 砍价异常, remark={user_config.bar_gain_state.remark},开始处理暂停策略")
    update_bargain_state(user_config)
    log.info(
        f"name:{user_config.name} 当前城市：{user_config.bar_gain_state.city}，当前pageNum：{user_config.bar_gain_state.page_num}，queue剩余数量：{task_queue.qsize()}")
    if task_queue.empty():
        log.info(f"name:{user_config.name} 暂停策略：当前队列为空")
        return
    data = []
    while not task_queue.empty():
        activity = task_queue.get()
        data.append(json.dumps(activity.to_dict()))
    conn = get_redis_connection()
    conn.lpush(f"{pause_pre_fix}{user_config.user_id}", *data)
    # 计算今天剩余秒数（到24点）
    now = datetime.datetime.now()
    expire_time = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)
    expire_seconds = int((expire_time - now).total_seconds())
    conn.expire(f"{pause_pre_fix}{user_config.user_id}", expire_seconds)
    log.info(f"name:{user_config.name} save task_queue success, size: {len(data)}")


def update_bargain_state(user_config: UserConfig):
    log.info(
        f"name:{user_config.name}，保存执行进度 status:{user_config.bar_gain_state.status}, city_name:{user_config.bar_gain_state.city}, page_num:{user_config.bar_gain_state.page_num}")
    user_config.bar_gain_state.current_time = datetime.datetime.now()
    thread_pool.submit(user_config_service.update_user_config_bargain_state, user_config.user_id,
                       user_config.bar_gain_state)


def is_today(date1):
    now = datetime.datetime.now()
    return date1.year == now.year and date1.month == now.month and date1.day == now.day
