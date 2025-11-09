import hashlib
import datetime
from typing import Dict, List, Any


def generate_rq_token(url_: str, data_: Dict[str, Any], user_id: int = None, ) -> str:
    try:
        # 1. 处理参数获取RTP
        rtp_map = _get_rtp(url_, user_id, data_)

        # 2. 对参数键进行排序
        sorted_keys: List[str] = sorted(rtp_map.keys())

        # 3. 拼接参数键值对字符串
        param_string = "&".join([f"{key}={rtp_map[key]}" for key in sorted_keys])

        # 4. 获取加密盐值
        salt = _generate_salt()

        # 5. 获取当前日期（yyyyMMdd）
        date = datetime.datetime.now().strftime("%Y%m%d")

        # 6. 拼接待加密字符串
        plain_text = f"{salt}#{url_}-{param_string}~{date}"

        # 7. MD5加密并返回结果
        return _md5(plain_text)
    except Exception as e:
        raise RuntimeError("生成rqtoken失败", e)


def _get_rtp(url_: str, user_id: int, data_: Dict[str, Any]) -> Dict[str, Any]:
    rtp_map = data_.copy()

    # 根据URL处理参数
    if url_ == "/api/shop/bargainings_ws":
        # 移除unmi参数，并添加id参数
        rtp_map.pop("unmi", None)
        rtp_map["id"] = user_id
    elif url_ == "/api/shop/activity":
        # 重构参数为p和c
        new_map = {
            "p": rtp_map.get("page"),
            "c": rtp_map.get("city", "bj")
        }
        rtp_map = new_map
    elif url_ == "/api/user/thirds":
        # 只保留code参数
        rtp_map = {"code": rtp_map.get("code")}
    # 其他url的处理规则需要根据实际业务补充+

    else:
        # 默认不做特殊处理
        pass

    return rtp_map


def _generate_salt() -> str:
    # 对应Java代码中的盐值
    return "JSTtT*(lvlv!#^&%~~"


def _md5(input_str: str) -> str:
    # MD5加密，返回32位小写字符串
    md5_hash = hashlib.md5()
    md5_hash.update(input_str.encode('utf-8'))
    return md5_hash.hexdigest()


# 测试方法
if __name__ == "__main__":
    data = {
        "yq_user_id": "",
        "activitygoods_id": "",
        "token": "",
        "unmi": "6665"
    }
    url = "/api/shop/bargainings_ws"
    print(generate_rq_token(url, data, None))
