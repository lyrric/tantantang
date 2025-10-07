from typing import List

import aiohttp
import tantantang.logging_config
from tantantang.models import Activity, HttpResult

log = tantantang.logging_config.get_logger(__name__)

BASE_URL = 'https://ttt.bjlxkjyxgs.cn'


async def activity(cate_id=0, cate2_id=0, title=None, page=1, limit=10,
                   lon=None, lat=None, city=None, area=None, street=None,
                   req_token=None, token=None) -> list[Activity]:
    """
    :param cate_id: 跟第一个筛选有关系
    :param cate2_id:
    :param title: 搜索关键字
    :param page: 分页
    :param limit: 分页
    :param lon: 经纬度
    :param lat: 经纬度
    :param city: 城市
    :param area 地区
    :param street 街道
    :param req_token: 貌似跟city有关系，city不一样，这个参数也不一样，这个参数跟session是没啥关系的。
    :param token: 用户token
    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(BASE_URL + "/api/shop/activity", data={
            "cate_id": cate_id,
            "cate2_id": cate2_id,
            "page": page,
            "count": limit,
            "lon": lon,
            "lat": lat,
            "title": title,
            "area": area,
            "street": street,
            "city": city,
            "req_token": req_token
        },
                                headers=get_headers(token)) as response:
            if response.ok:
                result_dict = await response.json()
                code = result_dict['code']
                if code == 1:
                    data_list = result_dict['data']['data']
                    result: List[Activity] = [Activity.from_dict(data) for data in data_list]
                    return result
                else:
                    raise Exception(f"获取活动列表失败 {result_dict['msg']}")
            else:
                log.warn(f"获取活动列表失败 {response.reason}")
                raise Exception(f"获取活动列表失败 {response.reason}")


#砍价
async def bar_gain(token, activitygoods_id) -> HttpResult:
    """
    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(BASE_URL + "/api/shop/activity",
                                data={
                                    "activitygoods_id": activitygoods_id
                                },
                                headers=get_headers(token)) as response:
            if response.ok:
                result_dict = await response.json()
                code = result_dict['code']
                if code == 1:
                    data = result_dict['data']
                    result = HttpResult.ok(data)
                    return result
                else:
                    raise Exception(f"获取活动列表失败 {result_dict['msg']}")
            else:
                log.warn(f"获取活动列表失败 {response.reason}")
                raise Exception(f"获取活动列表失败 {response.reason}")


def get_headers(token):
    return {"token": token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf2541022) XWEB/16467",
            "Referer": "https://servicewechat.com/wx454addfc6819a2ac/115/page-frame.html",
            }
