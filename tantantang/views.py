import asyncio
import json
import time
import threading

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tantantang import ttt_http
from tantantang.models import UserConfig, HttpResult, BarGainState
from tantantang import scheduled_task
from tantantang.user_config_service import (
    add_user_config,
    get_all_user_configs,
    get_user_config_by_uid,
    update_user_config_by_uid,
    delete_user_config_by_uid
)
from tantantang.exceptions import UserConfigNotFoundException


@csrf_exempt
def create_user_config(request):
    """
    创建用户配置
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        user_config = UserConfig.from_dict(data)
        user_config.bar_gain_state = BarGainState.from_default(user_config.user_id)
        asyncio.run(add_user_config(user_config))
        return JsonResponse(HttpResult.ok().to_dict())
    else:
        return JsonResponse(HttpResult.error('Method not allowed').to_dict(), status=405)


def get_user_configs(request):
    """
    获取所有用户配置
    """
    if request.method == 'GET':
        user_configs = get_all_user_configs()
        configs_data = []
        for config in user_configs:
            configs_data.append(config.to_dict())
        return JsonResponse(HttpResult.ok(configs_data).to_dict())
    else:
        return JsonResponse(HttpResult.error('Method not allowed').to_dict(), status=405)


@csrf_exempt
def update_user_config(request, user_id):
    """
    根据UID更新用户配置
    """
    if request.method == 'PUT':
        data = json.loads(request.body)
        updated_config = UserConfig.from_dict(data)

        update_user_config_by_uid(updated_config)
        return JsonResponse(HttpResult.ok().to_dict())
    else:
        return JsonResponse(HttpResult.error('Method not allowed').to_dict(), status=405)


@csrf_exempt
def delete_user_config(request, user_id):
    """
    根据UID删除用户配置
    """
    if request.method == 'DELETE':
        delete_user_config_by_uid(user_id)
        return JsonResponse(HttpResult.ok().to_dict())
    else:
        return JsonResponse(HttpResult.error('Method not allowed').to_dict(), status=405)


# 立即运行砍价
@csrf_exempt
def start_bargain(request, user_id: int):
    user_config = get_user_config_by_uid(user_id)
    if user_config is not None:
        # 在新线程中执行任务
        thread = threading.Thread(target=lambda: asyncio.run(scheduled_task.start_one(user_config)))
        thread.start()
        return JsonResponse(HttpResult.ok().to_dict(), status=200)
    else:
        # 使用自定义异常
        raise UserConfigNotFoundException('UserConfig not found')


async def get_activity_list(request, user_id: int):
    # 获取GET请求中的参数
    page_num = request.GET.get('page_num', 1)  # 默认值为1
    page_size = request.GET.get('page_size', 10)  # 默认值为10
    user_config = get_user_config_by_uid(user_id)
    if user_config is None:
        # 使用自定义异常
        raise UserConfigNotFoundException('UserConfig not found')
    
    activities = await ttt_http.get_activity_list(
        page_num, page_size, user_config.city, 
        user_config.lnt, user_config.lat
    )
    dict_list = [activity.to_dict() for activity in activities]
    return JsonResponse(HttpResult.ok(dict_list).to_dict())