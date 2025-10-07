import json
import time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from tantantang.models import UserConfig, HttpResult
from tantantang.user_config import (
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
        try:
            data = json.loads(request.body)
            # 使用当前时间戳（毫秒级）作为uid
            current_timestamp = int(time.time() * 1000)
            user_config = UserConfig.from_dict(data)
            user_config.uid = current_timestamp
            add_user_config(user_config)
            return JsonResponse(HttpResult.ok().to_dict())
        except Exception as e:
            return JsonResponse(HttpResult.error(str(e)).to_dict(), status=400)
    else:
        return JsonResponse(HttpResult.error('Method not allowed').to_dict(), status=405)


def get_user_configs(request):
    """
    获取所有用户配置
    """
    if request.method == 'GET':
        try:
            user_configs = get_all_user_configs()
            configs_data = []
            for config in user_configs:
                configs_data.append(config.to_dict())
            return JsonResponse(HttpResult.ok(configs_data).to_dict())
        except Exception as e:
            return JsonResponse(HttpResult.error(str(e)).to_dict(), status=500)
    else:
        return JsonResponse(HttpResult.error('Method not allowed').to_dict(), status=405)


def get_user_config(request, uid):
    """
    根据UID获取特定用户配置
    """
    if request.method == 'GET':
        try:
            user_config = get_user_config_by_uid(uid)
            if user_config:
                config_data = user_config.to_dict()
                return JsonResponse(HttpResult.ok(config_data).to_dict())
            else:
                return JsonResponse(HttpResult.error('UserConfig not found').to_dict(), status=404)
        except Exception as e:
            return JsonResponse(HttpResult.error(str(e)).to_dict(), status=500)
    else:
        return JsonResponse(HttpResult.error('Method not allowed').to_dict(), status=405)


@csrf_exempt
def update_user_config(request, uid):
    """
    根据UID更新用户配置
    """
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            updated_config = UserConfig.from_dict(data)

            success = update_user_config_by_uid(uid, updated_config)
            if success:
                return JsonResponse(HttpResult.ok().to_dict())
            else:
                return JsonResponse(HttpResult.error('UserConfig not found').to_dict(), status=404)
        except Exception as e:
            return JsonResponse(HttpResult.error(str(e)).to_dict(), status=400)
    else:
        return JsonResponse(HttpResult.error('Method not allowed').to_dict(), status=405)


@csrf_exempt
def delete_user_config(request, uid):
    """
    根据UID删除用户配置
    """
    if request.method == 'DELETE':
        try:
            success = delete_user_config_by_uid(uid)
            if success:
                return JsonResponse(HttpResult.ok().to_dict())
            else:
                return JsonResponse(HttpResult.error('UserConfig not found').to_dict(), status=404)
        except Exception as e:
            return JsonResponse(HttpResult.error(str(e)).to_dict(), status=500)
    else:
        return JsonResponse(HttpResult.error('Method not allowed').to_dict(), status=405)
