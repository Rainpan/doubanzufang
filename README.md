### doubanzufang
根据python脚本改编的爬取豆瓣小组内租房信息，根据自己需求筛选

### 功能点
1. 字典配置化
   - 包含爬取地址、白名单、黑名单、推送关键词、一二级排除词配置，可禁用启用
2. 关键字匹配
   - 筛选词 - 白名单词
   - 推送词 - 包含则微信/TG通知
   - 一级排除 - 首要过滤的词，包含则排除
   - 二级排除 - 包含则排除，否则存为备用数据
   - 黑名单词 - 包含则发帖人加入到黑名单
3. 黑名单维护
   - 排除黑名单中发的帖子
4. 微信通知
   -如果包含推送关键词，则利用server酱把标题和地址推送到微信
5. 过滤疑似中介公寓
   - 通过计算以及公共标识，判断是否为中介公寓，如果是则把发帖人加入到黑名单，帖子pass
6. 过滤发帖人重复发帖
   - 过滤同一用户发好几个同样的帖子
7. 页面查看配置
   - 可在页面查看爬取结果列表或配置字典表
8. 定时任务
   - 每小时执行一次
9. 其他
   - 收藏操作 - 帖子收藏
   - 删除操作 - 帖子状态置为删除
   - 手动标记中介公寓 - 发帖人加入黑名单，帖子删除并标记为中介公寓

# 暂停功能
1. 代理
   - 代理需要自己加，免费代理池效果太差，影响爬取结果
