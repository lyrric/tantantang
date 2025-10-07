import datetime
import tantantang.logging_config
from tantantang import user_config_service
from tantantang.models import UserConfig
from tantantang.models import City
from tantantang import ttt_http
log = tantantang.logging_config.get_logger(__name__)


def start():
    log.info(f"开始执行")
    user_configs = user_config_service.get_all_user_configs()
    user_configs = [user_config for user_config in user_configs if user_config.auto_bargain]
    log.info(f"开始执行，共{len(user_configs)}")
    for user_config in user_configs:
        user_config_service.update_user_config_by_uid(user_config.uid, user_config)


cities:list[City] = []

async def start_one(user_config:UserConfig):
    log.info(f"开始执行自动砍价：{user_config.name}")
    try:
        success_count = 0
        failed_count = 0
        #获取的糖果数量
        tg:float = 0
        for city in cities:
            log.info(f"开始执行城市:{city.name}")
            city_count = 0
            for i in range(1, 10):
                log.info(f"开始执行第{i}页")
                activities = await ttt_http.activity(page = i + 1, city=city.name, req_token=city.req_token)
                if len(activities) == 0:
                    break
                for activity in activities:
                    try:
                        result = await ttt_http.bar_gain(activity.activitygoods_id, user_config.token)
                        log.info(f"activity_id{activity.activity_id}, name: {activity.shop_name}，砍价完成")
                        if result.code == 200:
                            success_count += 1
                            city_count += 1
                            tg += result.data
                        else:
                            failed_count += 1
                    except Exception as e:
                        log.error(f"自动砍价失败：{user_config.name}")
                log.info(f"第{i}页执行完成")
            log.info(f"城市:{city.name}，执行完成，执行数量：{city_count}")
        log.info(f"name:{user_config.name}，执行完成，成功：{success_count}，失败：{failed_count}，获得糖果数量：{tg}")
    except Exception as e:
        log.error(f"自动砍价失败：{user_config.name}")
    finally:
        log.info(f"砍价执行完成：{user_config.name}")

