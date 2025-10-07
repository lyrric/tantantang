from django.db import models


# 活动列表
class Activity:
    def __init__(self, activitygoods_id: int = None, activity_id: int = None, createtime: int = None,
                 first_price: float = None,
                 title: str = None, hot: int = None, y_price: float = None, price: float = None, shop_name: str = None,
                 is_stop: int = None,
                 is_sell=None, sy_store=None, is_top=None, sales_volume=None, kj_num: int = None,
                 lon: float = None, lat: float = None, rank3=None, is_m_shop=None, image: str = None, share_image=None,
                 tags=None, distance: float = None, is_cut: int = None, kan: int = None, is_tag=None):
        """
        :param activitygoods_id: 商品id
        :param activity_id: 活动id
        :param createtime: 创建时间戳，秒级
        :param first_price: 价格，有时候为0，有时候跟price，暂时不用
        :param title: 标题
        :param hot: 热度
        :param y_price: 原价
        :param price: 当前价格
        :param shop_name: 门店名称
        :param is_stop: 一般为1
        :param is_sell: 一般为1
        :param sy_store: 库存数量
        :param is_top: 一般为0
        :param sales_volume:
        :param kj_num: 砍价次数
        :param lon: 经度
        :param lat: 纬度
        :param rank3:
        :param is_m_shop:
        :param image: 图片
        :param share_image:
        :param tags:
        :param distance: 距离，米
        :param is_cut: 是否已砍，为2：未砍，1：已砍
        :param kan: 是否还能再砍，1表示不能砍，0：表示可以
        :param is_tag:
        """
        self.activitygoods_id = activitygoods_id
        self.activity_id = activity_id
        self.createtime = createtime
        self.first_price = first_price
        self.title = title
        self.hot = hot
        self.y_price = y_price
        self.price = price
        self.shop_name = shop_name
        self.is_stop = is_stop
        self.is_sell = is_sell
        self.sy_store = sy_store
        self.is_top = is_top
        self.sales_volume = sales_volume
        self.kj_num = kj_num
        self.lon = lon
        self.lat = lat
        self.rank3 = rank3
        self.is_m_shop = is_m_shop
        self.image = image
        self.share_image = share_image
        self.tags = tags if tags is not None else []
        self.distance = distance
        self.is_cut = is_cut
        self.kan = kan
        self.is_tag = is_tag

    @classmethod
    def from_dict(cls, data: dict):
        """
        从字典创建Activity实例
        :param data: 包含Activity属性的字典
        :return: Activity实例
        """
        return cls(
            activitygoods_id=data.get('activitygoods_id'),
            activity_id=data.get('activity_id'),
            createtime=data.get('createtime'),
            first_price=data.get('first_price'),
            title=data.get('title'),
            hot=data.get('hot'),
            y_price=data.get('y_price'),
            price=data.get('price'),
            shop_name=data.get('shop_name'),
            is_stop=data.get('is_stop'),
            is_sell=data.get('is_sell'),
            sy_store=data.get('sy_store'),
            is_top=data.get('is_top'),
            sales_volume=data.get('sales_volume'),
            kj_num=data.get('kj_num'),
            lon=data.get('lon'),
            lat=data.get('lat'),
            rank3=data.get('rank3'),
            is_m_shop=data.get('is_m_shop'),
            image=data.get('image'),
            share_image=data.get('share_image'),
            tags=data.get('tags', []),
            distance=data.get('distance'),
            is_cut=data.get('is_cut'),
            kan=data.get('kan'),
            is_tag=data.get('is_tag')
        )

    def __str__(self):
        return f"Activity(title='{self.title}', price={self.price}, shop_name='{self.shop_name}, sy_store='{self.sy_store}')"


# 用户配置
class UserConfig:
    def __init__(self, name: str, uid: int = None, token: str = None, city: str = None, spt: str = None,
                 lnt: float = None,
                 lat: float = None, auto_bargain: bool = False):
        """
        :param name: 名称
        :param uid: uid 毫秒级时间戳
        :param token: token
        :param city: 城市
        :param spt: 推送spt
        :param lnt: 纬度
        :param lat: 经度
        :param auto_bargain: 是否自动砍价，默认为False
        """
        self.name = name
        self.uid = uid
        self.token = token
        self.city = city
        self.spt = spt
        self.lnt = lnt
        self.lat = lat
        self.auto_bargain = auto_bargain

    @classmethod
    def from_dict(cls, data: dict):
        """
        从字典创建UserConfig实例
        :param data: 包含UserConfig属性的字典
        :return: UserConfig实例
        """
        return cls(
            name=data.get('name'),
            uid=data.get('uid'),
            token=data.get('token'),
            city=data.get('city'),
            spt=data.get('spt'),
            lnt=data.get('lnt'),
            lat=data.get('lat'),
            auto_bargain=data.get('auto_bargain', False)
        )

    def __str__(self):
        return f"UserConfig(_id={self.uid}, name='{self.name}', city='{self.city}')"

    def to_dict(self):
        """
        将UserConfig实例转换为字典
        :return: 包含UserConfig所有属性的字典
        """
        return {
            "uid": self.uid,
            "name": self.name,
            "token": self.token,
            "city": self.city,
            "spt": self.spt,
            "lnt": self.lnt,
            "lat": self.lat,
            "auto_bargain": self.auto_bargain
        }


class HttpResult:
    """
    HTTP结果
    code: 状态码200 ok
    msg: 错误消息
    data： 数据
    """

    def __init__(self, code, msg, data):
        self.code = code
        self.data = data
        self.msg = msg

    def to_dict(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }

    @classmethod
    def ok(cls, data=None):
        return cls(200, "ok", data)

    @classmethod
    def error(cls, msg):
        return cls(500, msg, None)

    def __str__(self):
        return f"HttpResult(code={self.code}, msg={self.msg}, data={self.data})"


class City:
    def __init__(self, name, req_token):
        self.name = name
        self.req_token = req_token