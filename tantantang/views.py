import asyncio
import json
import threading

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection

from tantantang import ttt_http
from tantantang import ttt_task
from tantantang.exceptions import BusinessException
from tantantang.models import UserConfig, HttpResult, BarGainState, MonitorActivity
from tantantang.monitor_activity_service import (
    add_monitor_activity,
    get_all_monitor_activities,
    update_monitor_activity_by_id,
    delete_monitor_activity_by_id
)
from tantantang.user_config_service import (
    add_user_config,
    get_all_user_configs,
    get_user_config_by_uid,
    update_user_config_by_uid,
    delete_user_config_by_uid
)


@csrf_exempt
def create_user_config(request):
    """
    创建用户配置
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        user_config = UserConfig.from_dict(data)
        user_config.bar_gain_state = BarGainState.from_default()
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
        start = data.get("start")
        if start:
            start_bargain(None, user_id)
        return JsonResponse(HttpResult.ok().to_dict())
    else:
        return JsonResponse(HttpResult.error('Method not允许').to_dict(), status=405)


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


@csrf_exempt
def start_bargain(request, user_id: int):
    """
    开始砍价
    """
    user_config = get_user_config_by_uid(user_id)
    if user_config is not None:
        # 在新线程中执行任务
        thread = threading.Thread(target=lambda: asyncio.run(ttt_task.start_one(user_config)))
        thread.start()
        return JsonResponse(HttpResult.ok().to_dict(), status=200)
    else:
        # 使用自定义异常
        raise BusinessException('配置不存在')


def get_activity_list(request, user_id: int):
    """
    获取砍价列表
    """
    if request.method == 'GET':
        page_num = request.GET.get('page_num', 1)  # 默认值为1
        page_size = request.GET.get('page_size', 10)  # 默认值为10
        title = request.GET.get('title')  # 搜索key
        user_config = get_user_config_by_uid(user_id)
        if user_config is None:
            # 使用自定义异常
            raise BusinessException('配置不存在')

        activities = asyncio.run(ttt_http.get_activity_list(
            page_num, page_size, user_config.city,
            lon=user_config.lnt, lat=user_config.lat,
            title=title, token=user_config.token
        ))
        dict_list = [activity.to_dict() for activity in activities]
        return JsonResponse(HttpResult.ok(dict_list).to_dict())
    else:
        return JsonResponse(HttpResult.error('Method not allowed').to_dict(), status=405)


@csrf_exempt
def create_monitor_activity(request):
    """
    创建监控活动
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        monitor_activity = MonitorActivity.from_dict(data)
        m_id = add_monitor_activity(monitor_activity)
        return JsonResponse(HttpResult.ok({"m_id": m_id}).to_dict())
    else:
        return JsonResponse(HttpResult.error('Method not allowed').to_dict(), status=405)


def get_monitor_activities(request):
    """
    获取所有监控活动
    """
    if request.method == 'GET':
        monitor_activities = get_all_monitor_activities()
        activities_data = []
        for activity in monitor_activities:
            activities_data.append(activity.to_dict())
        return JsonResponse(HttpResult.ok(activities_data).to_dict())
    else:
        return JsonResponse(HttpResult.error('Method not allowed').to_dict(), status=405)


@csrf_exempt
def update_monitor_activity(request, m_id):
    """
    根据ID更新监控活动
    """
    if request.method == 'PUT':
        data = json.loads(request.body)
        # 确保URL中的m_id与数据中的m_id一致
        data['m_id'] = m_id
        updated_activity = MonitorActivity.from_dict(data)
        success = update_monitor_activity_by_id(updated_activity)
        if success:
            return JsonResponse(HttpResult.ok().to_dict())
        else:
            return JsonResponse(HttpResult.error('监控活动不存在').to_dict(), status=404)
    else:
        return JsonResponse(HttpResult.error('Method not allowed').to_dict(), status=405)


@csrf_exempt
def delete_monitor_activity(request, m_id):
    """
    根据ID删除监控活动
    """
    if request.method == 'DELETE':
        success = delete_monitor_activity_by_id(m_id)
        if success:
            return JsonResponse(HttpResult.ok().to_dict())
        else:
            return JsonResponse(HttpResult.error('监控活动不存在').to_dict(), status=404)
    else:
        return JsonResponse(HttpResult.error('Method not allowed').to_dict(), status=405)


def test(request):
    conn = get_redis_connection()
    user_config = get_user_config_by_uid(1286827)
    if user_config is not None:
        conn.hset("test123", "123", json.dumps(user_config.to_dict()))
    return JsonResponse(HttpResult.ok().to_dict())
