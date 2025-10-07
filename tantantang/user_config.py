from typing import List

from django_redis import get_redis_connection
import json
from tantantang.models import UserConfig


def _user_config_key():
    """获取UserConfig在Redis中存储的hash key"""
    return "USER_CONFIGS"


def add_user_config(user_config: UserConfig):
    """
    添加用户配置到Redis hash
    :param user_config: UserConfig实例
    """
    conn = get_redis_connection()
    key = _user_config_key()

    # 将UserConfig对象转换为字典，再序列化为JSON字符串
    user_config_dict = user_config.to_dict()

    user_config_json = json.dumps(user_config_dict)
    # 在hash中存储用户配置详情，使用uid作为field
    conn.hset(key, user_config.uid, user_config_json)


def get_all_user_configs() -> List[UserConfig]:
    """
    获取所有用户配置
    :return: UserConfig对象列表
    """
    conn = get_redis_connection()
    key = _user_config_key()

    # 获取所有用户配置
    user_configs_dict = conn.hgetall(key)

    user_configs: List[UserConfig] = []
    for uid, user_config_json in user_configs_dict.items():
        # 将JSON字符串转换为字典
        user_config_dict = json.loads(user_config_json)
        # 创建UserConfig对象
        user_config = UserConfig.from_dict(user_config_dict)
        user_configs.append(user_config)

    return user_configs


def get_user_config_by_uid(uid: int):
    """
    根据uid获取用户配置
    :param uid: 用户配置uid
    :return: UserConfig对象或None
    """
    conn = get_redis_connection()
    key = _user_config_key()

    user_config_json = conn.hget(key, uid)
    if user_config_json:
        # 将JSON字符串转换为字典
        user_config_dict = json.loads(user_config_json)
        # 创建UserConfig对象
        user_config = UserConfig.from_dict(user_config_dict)
        return user_config
    return None


def update_user_config_by_uid(uid: int, updated_user_config: UserConfig):
    """
    根据uid更新用户配置
    :param uid: 要更新的用户配置uid
    :param updated_user_config: 新的UserConfig实例
    :return: bool 是否更新成功
    """
    # 先检查用户配置是否存在
    existing_config = get_user_config_by_uid(uid)
    if not existing_config:
        return False

    conn = get_redis_connection()
    key = _user_config_key()

    # 更新用户配置
    updated_dict = updated_user_config.to_dict()

    updated_json = json.dumps(updated_dict)
    conn.hset(key, uid, updated_json)
    return True


def delete_user_config_by_uid(uid: int):
    """
    根据uid删除用户配置
    :param uid: 要删除的用户配置uid
    :return: bool 是否删除成功
    """
    conn = get_redis_connection()
    key = _user_config_key()

    # 删除hash中的数据
    result = conn.hdel(key, uid)

    # 返回是否删除成功
    return result > 0
