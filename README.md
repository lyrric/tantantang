# 探探糖

自动砍价脚本

## 使用方法

- 环境变量配好REDIS_HOST和REDIS_PASSWORD
- token参数抓包，在header头里面。
- key参数在/api/user/thirds接口，只有第一次登陆才会调用。或者点击砍价，请求参数里面的token及为key

## 待完成

- [ ] 运行结束通知
- [ ] 实时查看运行状态
- [ ] 定时运行
- [ ] 监控所有商品
- [ ] 监控单个商品

## 更新记录

- 2025-10-09 自动砍价功能基本能用

## 杂谈

- req_token为加密参数，加密跟请求参数有关系，加密逻辑在rq_token_util.py
- header头的token才是用户会话token
- 砍价接口会额外带一个token，这个token过期或者无效会导致砍价成功，但是得不到糖果