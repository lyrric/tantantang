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
        :param is_top: 一般为0 是否置顶
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

    def to_dict(self):
        """
        将Activity实例转换为字典
        :return: 包含Activity所有属性的字典
        """
        return {
            "activitygoods_id": self.activitygoods_id,
            "activity_id": self.activity_id,
            "createtime": self.createtime,
            "first_price": self.first_price,
            "title": self.title,
            "hot": self.hot,
            "y_price": self.y_price,
            "price": self.price,
            "shop_name": self.shop_name,
            "is_stop": self.is_stop,
            "is_sell": self.is_sell,
            "sy_store": self.sy_store,
            "is_top": self.is_top,
            "sales_volume": self.sales_volume,
            "kj_num": self.kj_num,
            "lon": self.lon,
            "lat": self.lat,
            "rank3": self.rank3,
            "is_m_shop": self.is_m_shop,
            "image": self.image,
            "share_image": self.share_image,
            "tags": self.tags,
            "distance": self.distance,
            "is_cut": self.is_cut,
            "kan": self.kan,
            "is_tag": self.is_tag
        }


# 砍价状态
class BarGainState:
    """
    砍价状态
    """

    def __init__(self, status=1, city=None, page_num=None, current_time=None, remark=None):
        """
        初始化BarGainState实例
        :param status: 状态 1：未开始，2：进行中，3：暂停，4：已完成
        :param city: 城市名称
        :param page_num: 页码
        :param current_time: 当前时间
        :param remark: 额外信息，一般为砍价失败原因
        """
        self.status = status
        self.city = city
        self.page_num = page_num
        self.current_time = current_time
        self.remark = remark

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
            status=data.get('status'),
            city=data.get('city'),
            page_num=data.get('page_num'),
            current_time=current_time,
            remark=data.get('remark')
        )

    @classmethod
    def from_default(cls):
        return cls(
            status=1
        )

    def __str__(self):
        return f"BarGainState(status={self.status}, city='{self.city}', page_num={self.page_num}, remark='{self.remark}')"

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
            "status": self.status,
            "city": self.city,
            "page_num": self.page_num,
            "current_time": current_time,
            "remark": self.remark
        }


# 用户配置
class UserConfig:
    def __init__(self, name: str, user_id: int = None, token: str = None, city: str = None, spt: str = None,
                 lnt: float = None, lat: float = None, key: str = None, bar_gain_state: BarGainState = None):
        """
        :param name: 名称
        :param token: token
        :param city: 城市
        :param spt: 推送spt
        :param lnt: 纬度
        :param lat: 经度
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


# 商品详情类
class Goods:
    def __init__(self, title: str = None, tags: str = None, content: str = None, content2: str = None,
                 content3: str = None, sell_intr: str = None, appl_stores_num: int = None, is_tag: int = None,
                 image_url: list = None, share_image_url: list = None, images_url: list = None):
        """
        :param title: 商品标题
        :param tags: 标签
        :param content: 内容
        :param content2: 内容2
        :param content3: 内容3
        :param sell_intr: 销售说明
        :param appl_stores_num: 适用店铺数
        :param is_tag: 标签标识
        :param image_url: 图片URL列表
        :param share_image_url: 分享图片URL列表
        :param images_url: 图片URL列表
        """
        self.title = title
        self.tags = tags
        self.content = content
        self.content2 = content2
        self.content3 = content3
        self.sell_intr = sell_intr
        self.appl_stores_num = appl_stores_num
        self.is_tag = is_tag
        self.image_url = image_url if image_url is not None else []
        self.share_image_url = share_image_url if share_image_url is not None else []
        self.images_url = images_url if images_url is not None else []

    @classmethod
    def from_dict(cls, data: dict):
        """
        从字典创建Goods实例
        :param data: 包含Goods属性的字典
        :return: Goods实例
        """
        return cls(
            title=data.get('title'),
            tags=data.get('tags'),
            content=data.get('content'),
            content2=data.get('content2'),
            content3=data.get('content3'),
            sell_intr=data.get('sell_intr'),
            appl_stores_num=data.get('appl_stores_num'),
            is_tag=data.get('is_tag'),
            image_url=data.get('image_url', []),
            share_image_url=data.get('share_image_url', []),
            images_url=data.get('images_url', [])
        )

    def __str__(self):
        return f"Goods(title='{self.title}', tags='{self.tags}')"

    def to_dict(self):
        """
        将Goods实例转换为字典
        :return: 包含Goods所有属性的字典
        """
        return {
            "title": self.title,
            "tags": self.tags,
            "content": self.content,
            "content2": self.content2,
            "content3": self.content3,
            "sell_intr": self.sell_intr,
            "appl_stores_num": self.appl_stores_num,
            "is_tag": self.is_tag,
            "image_url": self.image_url,
            "share_image_url": self.share_image_url,
            "images_url": self.images_url
        }


# 商店信息类
class Shop:
    def __init__(self, id: int = None, shop_name: str = None, prove_image: str = None, tags: str = None,
                 money: str = None, phone: str = None, address: str = None, lon: str = None, lat: str = None,
                 city_id: int = None, image_url: list = None, images_url: list = None, proveimage_url: list = None):
        """
        :param id: 商店ID
        :param shop_name: 商店名称
        :param prove_image: 认证图片
        :param tags: 标签
        :param money: 金额
        :param phone: 电话
        :param address: 地址
        :param lon: 经度
        :param lat: 纬度
        :param city_id: 城市ID
        :param image_url: 图片URL列表
        :param images_url: 图片URL列表
        :param proveimage_url: 认证图片URL列表
        """
        self.id = id
        self.shop_name = shop_name
        self.prove_image = prove_image
        self.tags = tags
        self.money = money
        self.phone = phone
        self.address = address
        self.lon = lon
        self.lat = lat
        self.city_id = city_id
        self.image_url = image_url if image_url is not None else []
        self.images_url = images_url if images_url is not None else []
        self.proveimage_url = proveimage_url if proveimage_url is not None else []

    @classmethod
    def from_dict(cls, data: dict):
        """
        从字典创建Shop实例
        :param data: 包含Shop属性的字典
        :return: Shop实例
        """
        return cls(
            id=data.get('id'),
            shop_name=data.get('shop_name'),
            prove_image=data.get('prove_image'),
            tags=data.get('tags'),
            money=data.get('money'),
            phone=data.get('phone'),
            address=data.get('address'),
            lon=data.get('lon'),
            lat=data.get('lat'),
            city_id=data.get('city_id'),
            image_url=data.get('image_url', []),
            images_url=data.get('images_url', []),
            proveimage_url=data.get('proveimage_url', [])
        )

    def __str__(self):
        return f"Shop(id={self.id}, shop_name='{self.shop_name}')"

    def to_dict(self):
        """
        将Shop实例转换为字典
        :return: 包含Shop所有属性的字典
        """
        return {
            "id": self.id,
            "shop_name": self.shop_name,
            "prove_image": self.prove_image,
            "tags": self.tags,
            "money": self.money,
            "phone": self.phone,
            "address": self.address,
            "lon": self.lon,
            "lat": self.lat,
            "city_id": self.city_id,
            "image_url": self.image_url,
            "images_url": self.images_url,
            "proveimage_url": self.proveimage_url
        }


# 活动信息类
class ActivityInfo:
    def __init__(self, id: int = None, rank3: str = None, is_m_shop: int = None, is_sell_text: str = None,
                 status_text: str = None):
        """
        :param id: 活动ID
        :param rank3: 排名
        :param is_m_shop: 是否主商店
        :param is_sell_text: 销售状态文本
        :param status_text: 状态文本
        """
        self.id = id
        self.rank3 = rank3
        self.is_m_shop = is_m_shop
        self.is_sell_text = is_sell_text
        self.status_text = status_text

    @classmethod
    def from_dict(cls, data: dict):
        """
        从字典创建ActivityInfo实例
        :param data: 包含ActivityInfo属性的字典
        :return: ActivityInfo实例
        """
        return cls(
            id=data.get('id'),
            rank3=data.get('rank3'),
            is_m_shop=data.get('is_m_shop'),
            is_sell_text=data.get('is_sell_text'),
            status_text=data.get('status_text')
        )

    def __str__(self):
        return f"ActivityInfo(id={self.id}, rank3='{self.rank3}')"

    def to_dict(self):
        """
        将ActivityInfo实例转换为字典
        :return: 包含ActivityInfo所有属性的字典
        """
        return {
            "id": self.id,
            "rank3": self.rank3,
            "is_m_shop": self.is_m_shop,
            "is_sell_text": self.is_sell_text,
            "status_text": self.status_text
        }


class ActivityDetail:
    """
    活动详情类
    """

    def __init__(self, id: int = None, user_id: int = None, activity_id: int = None, goods_id: int = None,
                 shop_id: int = None, title: str = None, y_price: str = None, price: str = None,
                 first_price: str = None, store: int = None, sy_store: int = None, hot: int = None,
                 is_sell: int = None, createtime: int = None, kan: int = None, goods: Goods = None,
                 shop: Shop = None, activity: ActivityInfo = None, is_sell_text: str = None,
                 grass: list = None, rice: float = None, is_cut: int = None):
        """
        :param id: ID
        :param user_id: 用户ID
        :param activity_id: 活动ID
        :param goods_id: 商品ID
        :param shop_id: 商店ID
        :param title: 标题
        :param y_price: 原价
        :param price: 当前价格
        :param first_price: 首次价格
        :param store: 库存
        :param sy_store: 剩余库存
        :param hot: 热度
        :param is_sell: 是否销售
        :param createtime: 创建时间戳
        :param kan: 是否可砍价
        :param goods: 商品信息
        :param shop: 商店信息
        :param activity: 活动信息
        :param is_sell_text: 销售状态文本
        :param grass: 草稿列表
        :param rice: 米数
        :param is_cut: 是否已砍价
        """
        self.id = id
        self.user_id = user_id
        self.activity_id = activity_id
        self.goods_id = goods_id
        self.shop_id = shop_id
        self.title = title
        self.y_price = y_price
        self.price = price
        self.first_price = first_price
        self.store = store
        self.sy_store = sy_store
        self.hot = hot
        self.is_sell = is_sell
        self.createtime = createtime
        self.kan = kan
        self.goods = goods
        self.shop = shop
        self.activity = activity
        self.is_sell_text = is_sell_text
        self.grass = grass if grass is not None else []
        self.rice = rice
        self.is_cut = is_cut

    @classmethod
    def from_dict(cls, data: dict):
        """
        从字典创建ActivityDetail实例
        :param data: 包含ActivityDetail属性的字典
        :return: ActivityDetail实例
        """
        goods = None
        if data.get('goods') is not None:
            goods = Goods.from_dict(data.get('goods'))

        shop = None
        if data.get('shop') is not None:
            shop = Shop.from_dict(data.get('shop'))

        activity = None
        if data.get('activity') is not None:
            activity = ActivityInfo.from_dict(data.get('activity'))

        return cls(
            id=data.get('id'),
            user_id=data.get('user_id'),
            activity_id=data.get('activity_id'),
            goods_id=data.get('goods_id'),
            shop_id=data.get('shop_id'),
            title=data.get('title'),
            y_price=data.get('y_price'),
            price=data.get('price'),
            first_price=data.get('first_price'),
            store=data.get('store'),
            sy_store=data.get('sy_store'),
            hot=data.get('hot'),
            is_sell=data.get('is_sell'),
            createtime=data.get('createtime'),
            kan=data.get('kan'),
            goods=goods,
            shop=shop,
            activity=activity,
            is_sell_text=data.get('is_sell_text'),
            grass=data.get('grass', []),
            rice=data.get('rice'),
            is_cut=data.get('is_cut')
        )

    def __str__(self):
        return f"ActivityDetail(id={self.id}, title='{self.title}', price={self.price},sy_store={self.sy_store})"

    def to_dict(self):
        """
        将ActivityDetail实例转换为字典
        :return: 包含ActivityDetail所有属性的字典
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "activity_id": self.activity_id,
            "goods_id": self.goods_id,
            "shop_id": self.shop_id,
            "title": self.title,
            "y_price": self.y_price,
            "price": self.price,
            "first_price": self.first_price,
            "store": self.store,
            "sy_store": self.sy_store,
            "hot": self.hot,
            "is_sell": self.is_sell,
            "createtime": self.createtime,
            "kan": self.kan,
            "goods": self.goods.to_dict() if self.goods else None,
            "shop": self.shop.to_dict() if self.shop else None,
            "activity": self.activity.to_dict() if self.activity else None,
            "is_sell_text": self.is_sell_text,
            "grass": self.grass,
            "rice": self.rice,
            "is_cut": self.is_cut
        }


class MonitorActivity:
    """
    监控活动
    """

    def __init__(self, m_type: int = None, shop_name: str = None, user_id: int = None, status: int = None):
        """
        :param m_type: 监控类型，1:低于某值时，每次降价提醒
        :param shop_name: 门店名称
        :param user_id: user_id
        :param status: 1:正常，2:暂停
        """
        self.m_type = m_type
        self.shop_name = shop_name
        self.user_id = user_id
        self.status = status

    @classmethod
    def from_dict(cls, data: dict):
        """
        从字典创建MonitorActivity实例
        :param data: 包含MonitorActivity属性的字典
        :return: MonitorActivity实例
        """
        return cls(
            m_type=data.get('m_type'),
            shop_name=data.get('shop_name'),
            user_id=data.get('user_id'),
            status=data.get('status')
        )

    def __str__(self):
        return f"MonitoringActivity(m_type={self.m_type}, shop_name='{self.shop_name}', user_id={self.user_id}, status={self.status})"

    def to_dict(self):
        """
        将MonitorActivity实例转换为字典
        :return: 包含MonitorActivity所有属性的字典
        """
        return {
            "m_type": self.m_type,
            "shop_name": self.shop_name,
            "user_id": self.user_id,
            "status": self.status
        }
