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
        return f"Activity(activitygoods_id={self.activitygoods_id},title='{self.title}', price={self.price}, shop_name='{self.shop_name}, sy_store='{self.sy_store}')"


# 砍价状态
class BarGainState:
    """
    砍价状态
    """

    def __init__(self, user_config_id: int, status=1, city=None, page_num=None, page_size=None, current_time=None):
        """
        初始化BarGainState实例
        :param user_config_id: 用户配置ID
        :param status: 状态 1：未开始，2：进行中，3：暂停，4：已完成
        :param city: 城市名称
        :param page_num: 页码
        :param page_size: 每页数量
        :param current_time: 当前时间
        """
        self.user_config_id = user_config_id
        self.status = status
        self.city = city
        self.page_num = page_num
        self.page_size = page_size
        self.current_time = current_time

    @classmethod
    def from_dict(cls, data: dict):
        """
        从字典创建BarGainStatus实例
        :param data: 包含BarGainStatus属性的字典
        :return: BarGainStatus实例
        """
        current_time = data.get('current_time')
        # 如果current_time是字符串，则转换为datetime对象
        if isinstance(current_time, str):
            try:
                import datetime
                current_time = datetime.datetime.fromisoformat(current_time)
            except ValueError:
                current_time = None

        return cls(
            user_config_id=data.get('user_config_id'),
            status=data.get('status'),
            city=data.get('city'),
            page_num=data.get('page_num'),
            page_size=data.get('page_size'),
            current_time=current_time
        )

    @classmethod
    def from_default(cls, user_config_id):
        return cls(
            user_config_id=user_config_id,
            status=1
        )

    def __str__(self):
        return f"BarGainState(user_config_id={self.user_config_id}, status={self.status}, city='{self.city}', page_num={self.page_num}, page_size={self.page_size})"

    def to_dict(self):
        """
        将BarGainState实例转换为字典
        :return: 包含BarGainState所有属性的字典
        """
        current_time = self.current_time
        if current_time is not None:
            # 将datetime对象转换为字符串格式，以便JSON序列化
            current_time = current_time.isoformat()

        return {
            "user_config_id": self.user_config_id,
            "status": self.status,
            "city": self.city,
            "page_num": self.page_num,
            "page_size": self.page_size,
            "current_time": current_time
        }


# 用户配置
class UserConfig:
    def __init__(self, name: str, user_id: int = None, token: str = None, city: str = None, spt: str = None,
                 lnt: float = None, lat: float = None,
                 auto_bargain: bool = False, key: str = None, bar_gain_state: BarGainState = None):
        """
        :param name: 名称
        :param token: token
        :param city: 城市
        :param spt: 推送spt
        :param lnt: 纬度
        :param lat: 经度
        :param auto_bargain: 是否自动砍价，默认为False
        :param user_id: 用户ID
        :param key: 砍价时用到的参数
        :param bar_gain_state: 砍价状态
        """
        self.name = name
        self.token = token
        self.city = city
        self.spt = spt
        self.lnt = lnt
        self.lat = lat
        self.auto_bargain = auto_bargain
        self.user_id = user_id
        self.key = key
        self.bar_gain_state = bar_gain_state

    @classmethod
    def from_dict(cls, data: dict):
        """
        从字典创建UserConfig实例
        :param data: 包含UserConfig属性的字典
        :return: UserConfig实例
        """
        bar_gain_state = None
        if data.get('bar_gain_state') is not None:
            bar_gain_state = BarGainState.from_dict(data.get('bar_gain_state'))
        return cls(
            name=data.get('name'),
            token=data.get('token'),
            city=data.get('city'),
            spt=data.get('spt'),
            lnt=data.get('lnt'),
            lat=data.get('lat'),
            auto_bargain=data.get('auto_bargain', False),
            user_id=data.get('user_id'),
            key=data.get('key'),
            bar_gain_state=bar_gain_state
        )

    def __str__(self):
        return f"UserConfig(_id={self.user_id}, name='{self.name}', city='{self.city}', user_id={self.user_id}, key='{self.key}')"

    def to_dict(self):
        """
        将UserConfig实例转换为字典
        :return: 包含UserConfig所有属性的字典
        """
        return {
            "name": self.name,
            "token": self.token,
            "city": self.city,
            "spt": self.spt,
            "lnt": self.lnt,
            "lat": self.lat,
            "auto_bargain": self.auto_bargain,
            "user_id": self.user_id,
            "key": self.key,
            "bar_gain_state": self.bar_gain_state.to_dict()
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


# 用户信息
class UserInfo:
    def __init__(self, id: int = None, group_id: int = None, username: str = None, nickname: str = None,
                 mobile: str = None, avatar: str = None, bio: str = None, score: int = None, is_vip: int = None,
                 province: str = None, city: str = None, area: str = None, fans: int = None, gz: int = None,
                 like: int = None, coll: int = None, lon: float = None, lat: float = None, last_time: str = None,
                 sign_count: int = None, sign_sum: int = None, idnum: str = None, is_sale: int = None,
                 all_money: int = None, have_money: int = None, give_money: int = None, b_card: int = None,
                 token: str = None, user_id: int = None, createtime: int = None, expiretime: int = None,
                 expires_in: int = None, have: int = None, daren: int = None, usable_coupon_num: int = None):
        """
        :param id: 用户ID
        :param group_id: 组ID
        :param username: 用户名 u+id
        :param nickname: 昵称
        :param mobile: 手机号
        :param avatar: 头像URL
        :param bio: 个人简介
        :param score: 糖果数量
        :param is_vip: 是否VIP
        :param province: 省份
        :param city: 城市
        :param area: 区域
        :param fans: 粉丝数
        :param gz: 关注数
        :param like: 点赞数
        :param coll: 收藏数
        :param lon: 经度
        :param lat: 纬度
        :param last_time: 最后登录时间
        :param sign_count: 签到次数
        :param sign_sum: 签到总次数
        :param idnum: ID编号
        :param is_sale: 是否销售人员
        :param all_money: 总金额
        :param have_money: 拥有金额
        :param give_money: 赠送金额
        :param b_card: B卡数量
        :param token: 用户token，也是6居然返回header头的token
        :param user_id: 用户ID
        :param createtime: 创建时间戳
        :param expiretime: 过期时间戳
        :param expires_in: 有效期
        :param have: 拥有数量
        :param daren: 是否达人
        :param usable_coupon_num: 可用优惠券数量
        """
        self.id = id
        self.group_id = group_id
        self.username = username
        self.nickname = nickname
        self.mobile = mobile
        self.avatar = avatar
        self.bio = bio
        self.score = score
        self.is_vip = is_vip
        self.province = province
        self.city = city
        self.area = area
        self.fans = fans
        self.gz = gz
        self.like = like
        self.coll = coll
        self.lon = lon
        self.lat = lat
        self.last_time = last_time
        self.sign_count = sign_count
        self.sign_sum = sign_sum
        self.idnum = idnum
        self.is_sale = is_sale
        self.all_money = all_money
        self.have_money = have_money
        self.give_money = give_money
        self.b_card = b_card
        self.token = token
        self.user_id = user_id
        self.createtime = createtime
        self.expiretime = expiretime
        self.expires_in = expires_in
        self.have = have
        self.daren = daren
        self.usable_coupon_num = usable_coupon_num

    @classmethod
    def from_dict(cls, data: dict):
        """
        从字典创建UserInfo实例
        :param data: 包含UserInfo属性的字典
        :return: UserInfo实例
        """
        return cls(
            id=data.get('id'),
            group_id=data.get('group_id'),
            username=data.get('username'),
            nickname=data.get('nickname'),
            mobile=data.get('mobile'),
            avatar=data.get('avatar'),
            bio=data.get('bio'),
            score=data.get('score'),
            is_vip=data.get('is_vip'),
            province=data.get('province'),
            city=data.get('city'),
            area=data.get('area'),
            fans=data.get('fans'),
            gz=data.get('gz'),
            like=data.get('like'),
            coll=data.get('coll'),
            lon=data.get('lon'),
            lat=data.get('lat'),
            last_time=data.get('last_time'),
            sign_count=data.get('sign_count'),
            sign_sum=data.get('sign_sum'),
            idnum=data.get('idnum'),
            is_sale=data.get('is_sale'),
            all_money=data.get('all_money'),
            have_money=data.get('have_money'),
            give_money=data.get('give_money'),
            b_card=data.get('b_card'),
            token=data.get('token'),
            user_id=data.get('user_id'),
            createtime=data.get('createtime'),
            expiretime=data.get('expiretime'),
            expires_in=data.get('expires_in'),
            have=data.get('have'),
            daren=data.get('daren'),
            usable_coupon_num=data.get('usable_coupon_num')
        )

    def __str__(self):
        return f"UserInfo(id={self.id}, username='{self.username}', nickname='{self.nickname}', score={self.score})"

    def to_dict(self):
        """
        将UserInfo实例转换为字典
        :return: 包含UserInfo所有属性的字典
        """
        return {
            "id": self.id,
            "group_id": self.group_id,
            "username": self.username,
            "nickname": self.nickname,
            "mobile": self.mobile,
            "avatar": self.avatar,
            "bio": self.bio,
            "score": self.score,
            "is_vip": self.is_vip,
            "province": self.province,
            "city": self.city,
            "area": self.area,
            "fans": self.fans,
            "gz": self.gz,
            "like": self.like,
            "coll": self.coll,
            "lon": self.lon,
            "lat": self.lat,
            "last_time": self.last_time,
            "sign_count": self.sign_count,
            "sign_sum": self.sign_sum,
            "idnum": self.idnum,
            "is_sale": self.is_sale,
            "all_money": self.all_money,
            "have_money": self.have_money,
            "give_money": self.give_money,
            "b_card": self.b_card,
            "token": self.token,
            "user_id": self.user_id,
            "createtime": self.createtime,
            "expiretime": self.expiretime,
            "expires_in": self.expires_in,
            "have": self.have,
            "daren": self.daren,
            "usable_coupon_num": self.usable_coupon_num
        }


# 城市信息
class City:
    def __init__(self, id: int = None, address: str = None, province: str = None, city: str = None,
                 createtime: int = None, code: int = None, status: int = None, qrcode: str = None,
                 welcome_pic: str = None, sort: int = None, icon_img: str = None):
        """
        :param id: 城市ID
        :param address: 地址（省份/城市）
        :param province: 省份
        :param city: 城市
        :param createtime: 创建时间戳
        :param code: 城市编码
        :param status: 状态
        :param qrcode: 二维码图片路径
        :param welcome_pic: 欢迎图片路径
        :param sort: 排序
        :param icon_img: 图标图片URL
        """
        self.id = id
        self.address = address
        self.province = province
        self.city = city
        self.createtime = createtime
        self.code = code
        self.status = status
        self.qrcode = qrcode
        self.welcome_pic = welcome_pic
        self.sort = sort
        self.icon_img = icon_img

    @classmethod
    def from_dict(cls, data: dict):
        """
        从字典创建City实例
        :param data: 包含City属性的字典
        :return: City实例
        """
        return cls(
            id=data.get('id'),
            address=data.get('address'),
            province=data.get('province'),
            city=data.get('city'),
            createtime=data.get('createtime'),
            code=data.get('code'),
            status=data.get('status'),
            qrcode=data.get('qrcode'),
            welcome_pic=data.get('welcome_pic'),
            sort=data.get('sort'),
            icon_img=data.get('icon_img')
        )

    def __str__(self):
        return f"City(id={self.id}, province='{self.province}', city='{self.city}', code={self.code})"

    def to_dict(self):
        """
        将City实例转换为字典
        :return: 包含City所有属性的字典
        """
        return {
            "id": self.id,
            "address": self.address,
            "province": self.province,
            "city": self.city,
            "createtime": self.createtime,
            "code": self.code,
            "status": self.status,
            "qrcode": self.qrcode,
            "welcome_pic": self.welcome_pic,
            "sort": self.sort,
            "icon_img": self.icon_img
        }
