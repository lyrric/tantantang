import datetime
import tantantang.logging_config
from tantantang import user_config_service
from tantantang.models import UserConfig
from tantantang.models import City
from tantantang import ttt_http
from tantantang.ttt_http import get_city_list

log = tantantang.logging_config.get_logger(__name__)


def start():
    log.info(f"开始执行")
    user_configs = user_config_service.get_all_user_configs()
    user_configs = [user_config for user_config in user_configs if user_config.auto_bargain]
    log.info(f"开始执行，共{len(user_configs)}")
    for user_config in user_configs:
        start_one(user_config)


async def start_one(user_config: UserConfig):
    log.info(f"开始执行自动砍价：{user_config.name}")
    success_count = 0
    # 获取的糖果数量
    tg: float = 0
    # 记录进度
    city_name: str = ''
    page_num: int = 1
    status = 2
    try:
        cities = await get_city_list()
        # 对城市列表按city字段进行排序
        cities.sort(key=lambda x: x.city)
        # 检查是否需要从上次的进度继续执行
        start_city_index = 0
        start_page_num = 1
        if user_config.bar_gain_state.status in [3]:
            # 根据进度确定起始城市和页码
            for i, city in enumerate(cities):
                if city.city == user_config.bar_gain_state.city:
                    start_city_index = i
                    start_page_num = user_config.bar_gain_state.page_num
                    break
        update_bargain_state(user_config, status, city_name, start_page_num)
        for city_index in range(start_city_index, len(cities)):
            city = cities[city_index]
            city_name = city.city
            log.info(f"开始执行城市:{city_name}")
            update_bargain_state(user_config, status, city_name, page_num)
            # 该城市的执行数量
            city_count = 0
            # 确定起始页码
            start_page = start_page_num if city_index == start_city_index else 1
            for page_num in range(start_page, 20):
                log.info(f"开始执行第{page_num}页")
                activities = await ttt_http.get_activity_list(page_num, 10, city_name, token=user_config.token)
                if len(activities) == 0:
                    break
                activities = [activity for activity in activities if
                              activity.kan == 0 and activity.is_cut == 2 and activity.sy_store > 0]
                for activity in activities:
                    score = await ttt_http.bar_gain(user_config.token, user_config.user_id, user_config.key,
                                                    activity.activitygoods_id)

                    if score is None:
                        status = 3
                        log.info(f"自动砍价失败：{activity} {user_config}")
                        return
                    elif score > 0:
                        success_count += 1
                        city_count += 1
                        tg += score
                    else:
                        # 等于0 表示砍价失败，但是可以继续执行
                        pass
                    log.info(
                        f"activity_id：{activity.activity_id}, name: {activity.shop_name}，砍价完成，获得糖果:{score}")
                log.info(f"第{page_num}页执行完成")
            log.info(f"城市:{city.city}，执行完成，执行数量：{city_count}")
            status = 4
    except Exception as e:
        log.error(f"自动砍价失败：{user_config.name}", exc_info=e)
        status = 3
    finally:
        log.info(f"name:{user_config.name}，执行完成，执行次数：{success_count}，获得糖果数量：{tg}")
        log.info(f"保存执行进度 status:{status}, city_name:{city_name}, page_num:{page_num}")
        update_bargain_state(user_config, status, city_name, page_num)


def update_bargain_state(user_config: UserConfig, status: int, city: str, page_num: int):
    user_config.bar_gain_state.status = status
    user_config.bar_gain_state.city = city
    user_config.bar_gain_state.page_num = page_num
    user_config.bar_gain_state.current_time = datetime.datetime.now()
    user_config_service.update_user_config_by_uid(user_config)
