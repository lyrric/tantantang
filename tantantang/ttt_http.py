import asyncio
from typing import Any

import aiohttp
from aiohttp import FormData
from aiohttp.web_fileresponse import content_type

import tantantang.logging_config
from tantantang.exceptions import BusinessException
from tantantang.models import Activity, City, ActivityDetail
from tantantang.models import UserInfo
from tantantang.rq_token_util import generate_rq_token

log = tantantang.logging_config.get_logger(__name__)

BASE_URL = 'https://ttt.bjlxkjyxgs.cn'


async def get_activity_list(page_num, page_size, city, lon=None, lat=None,
                            cate_id=None, cate2_id=0, title=None, area=None, street=None,
                            token=None) -> list[Activity]:
    """
    :param cate_id: 跟第一个筛选有关系
    :param cate2_id:
    :param title: 搜索关键字
    :param page_num: 分页
    :param page_size: 分页
    :param lon: 经纬度
    :param lat: 经纬度
    :param city: 城市
    :param area 地区
    :param street 街道
    :param token: 用户token
    :return:
    """
    data = {
        "lon": lon,
        "lat": lat,
        "area": area,
        "street": street,
        "cate_id": cate_id,
        "cate2_id": cate2_id,
        "page": page_num,
        "count": page_size,
        "city": city,
        "title": title
    }
    # 过滤掉值为None的数据
    data = {key: value for key, value in data.items() if value is not None}
    url = "/api/shop/activity"
    rq_token = generate_rq_token(url, data)
    data['rqtoken'] = rq_token
    async with aiohttp.ClientSession() as session:
        async with session.post(BASE_URL + url,
                                data=data,
                                headers=get_headers(token)) as response:
            if response.ok:
                result_dict = await response.json()
                code = result_dict['code']
                if code == 1:
                    data_list = result_dict['data']['data']
                    result: list[Activity] = [Activity.from_dict(data) for data in data_list]
                    return result
                else:
                    raise BusinessException(f"获取活动列表失败 {result_dict['msg']}")
            else:
                log.warn(f"获取活动列表失败 {response.reason}")
                raise BusinessException(f"获取活动列表失败 {response.reason}")


UNMI = 6665


# 砍价
async def bar_gain(token, user_id, user_key, activitygoods_id, yq_user_id='') -> Any | None:
    """
    :param yq_user_id: 可以为空
    :param token: token
    :param activitygoods_id: 商品id
    :param user_id 用户id
    :return: 获取的糖果数量，none表示失败
    """
    data = {
        "yq_user_id": yq_user_id,
        "token": user_key,
        "activitygoods_id": activitygoods_id,
        "unmi": UNMI
    }
    url = "/api/shop/bargainings_ws"
    rq_token = generate_rq_token(url, data, user_id=user_id)
    data['rqtoken'] = rq_token
    # 过滤掉值为None的数据
    async with aiohttp.ClientSession() as session:
        async with session.post(BASE_URL + url,
                                data=data,
                                headers=get_headers(token)) as response:
            if response.ok:
                result_dict = await response.json()
                code = result_dict['code']
                if code == 1:
                    data = result_dict['data']
                    score = data.get('score')
                    if score is None:
                        log.warn(f"获取糖果数量失败，应该是user_key过期了")
                        return None
                    return score
                else:
                    msg = result_dict['msg']
                    log.error(f"砍价失败 {msg}")
                    if '商品库存数不足' in msg:
                        return 0
                    if '当前砍价人数过多，请稍后砍价' in msg or '出差了' in msg:
                        await asyncio.sleep(5)
                        return 0
                    return None
            else:
                log.warn(f"砍价失败 {response.reason}")
                return None


# 获取用户信息
async def get_user_info(token, _type=1) -> UserInfo:
    """
    :param token:
    :param _type: 一般为1
    :return:
    """
    data = {
        "type": _type,
    }
    url = "/api/user/getuserinfo"
    rq_token = generate_rq_token(url, data)
    data['rqtoken'] = rq_token
    async with aiohttp.ClientSession() as session:
        async with session.post(BASE_URL + url, data=data,
                                headers=get_headers(token)) as response:
            if response.ok:
                result_dict = await response.json()
                code = result_dict['code']
                if code == 1:
                    return UserInfo.from_dict(result_dict['data'])
                else:
                    raise BusinessException(f"获取用户信息失败 {result_dict['msg']}")
            else:
                log.warn(f"获取用户信息失败 {response.reason}")
                raise BusinessException(f"获取用户信息失败 {response.reason}")


# 获取详细信息
async def get_activity_detail(token: str, activitygoods_id: int, lon: float, lat: float) -> ActivityDetail:
    """
    :param token:
    :param activitygoods_id:
    :param lon:
    :param lat:
    :return:
    """
    data = {
        "activitygoods_id": activitygoods_id,
        "lon": lon,
        "lat": lat,
    }
    url = "/api/shop/activity_detail"
    rq_token = generate_rq_token(url, data)
    data['rqtoken'] = rq_token
    async with aiohttp.ClientSession() as session:
        async with session.post(BASE_URL + url, data=data,
                                headers=get_headers(token)) as response:
            if response.ok:
                result_dict = await response.json()
                code = result_dict['code']
                if code == 1:
                    return ActivityDetail.from_dict(result_dict['data'])
                else:
                    raise BusinessException(f"获取活动详情失败 {result_dict['msg']}")
            else:
                log.warn(f"获取活动详情失败 {response.reason}")
                raise BusinessException(f"获取活动详情失败 {response.reason}")


def get_headers(token: str):
    token = token if token is not None else ''
    return {"token": token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf2541022) XWEB/16467",
            "Referer": "https://servicewechat.com/wx454addfc6819a2ac/115/page-frame.html",
            "Accept": "*/*",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Access-Control-Allow-Origin": "*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "xweb_xhr": "1",
            }


async def get_city_list() -> list[City]:
    async with aiohttp.ClientSession() as session:
        async with session.post(BASE_URL + "/api/index/get_city_list") as response:
            if response.ok:
                result_dict = await response.json()
                code = result_dict['code']
                if code == 1:
                    dicts = result_dict['data'].values()
                    return [City.from_dict(data) for data in dicts]
                else:
                    raise BusinessException(f"获取城市列表失败 {result_dict['msg']}")
            else:
                raise BusinessException(f"获取城市列表失败 {response.reason}")
