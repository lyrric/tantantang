import json

import aiohttp

from tantantang import logging_config

log = logging_config.get_logger(__name__)


async def send_message(spt, summary, content):
    if spt is None or spt == '':
        log.warn("未配置SPT，不发送消息")
        return
    body_map = {
        "content": content,
        "summary": summary,
        "contentType": 2,
        "spt": spt
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    "https://wxpusher.zjiecode.com/api/send/message/simple-push",
                    json=body_map,
                    ssl=False,
                    timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                result = await response.json()
                if result.get("code") != 1000:
                    log.error(f"发送消息失败: {result}")
    except Exception as e:
        log.error(f"发送消息失败: {e}")
