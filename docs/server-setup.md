# Server 酱推送配置教程

本教程将指导您如何配置 Server 酱进行消息推送。

## 为什么选择 Server 酱？

- ✅ **完全免费**：个人使用免费
- ✅ **配置简单**：只需一个 SendKey
- ✅ **多种通道**：支持微信、企业微信、钉钉等多种推送方式
- ✅ **稳定可靠**：官方服务，稳定性高

## 配置步骤

### 1. 注册 Server 酱

1. 访问 Server 酱官网：https://sct.ftqq.com/
2. 使用微信扫码登录
3. 登录后会自动创建一个 SendKey

### 2. 获取 SendKey

1. 登录后，在首页即可看到你的 SendKey
2. SendKey 格式类似：`SCT123456T1234567890AbCdEfGhIjKlMnOpQr`
3. 复制这个 SendKey

### 3. 配置到项目

将 SendKey 填入 `config.json`：

```json
{
  "account": {
    "name": "主账号",
    "host": "...",
    "li": "...",
    "idxgy": "...",
    "eoq": "...",
    "cookies": { ... }
  },
  "push": {
    "enabled": true,
    "sendkey": "SCT123456T1234567890AbCdEfGhIjKlMnOpQr"
  }
}
```

参数说明：
- `enabled`：是否启用推送（`true` 或 `false`）
- `sendkey`：你的 Server 酱 SendKey

### 4. 测试推送

运行签到程序测试：

```bash
python main.py
```

如果配置正确，签到完成后会收到微信推送通知。

## 推送效果

签到成功后，您将收到类似这样的微信消息：

```
古茗签到结果通知

📊 签到状态: ✅ 成功
👤 账户: 主账号
⏰ 时间: 2025-12-10 16:00:00

💬 结果: 签到成功！日期: 2025-12-10
📅 签到日期: 2025-12-10
```

## 常见问题

### Q1: 收不到推送消息？

**检查以下几点：**
1. 确认 SendKey 填写正确
2. 确认 `enabled` 设置为 `true`
3. 检查 Server 酱官网是否有推送记录
4. 查看程序运行日志是否有报错

### Q2: SendKey 在哪里找？

**获取方法：**
1. 登录 https://sct.ftqq.com/
2. 在首页即可看到 SendKey
3. 如果忘记了，可以重置 SendKey

### Q3: 可以发送给多个人吗？

**可以！** Server 酱支持多种推送通道：
1. 在 Server 酱后台配置多个消息通道
2. 可以同时推送到微信、钉钉、飞书等
3. 详见 Server 酱官网文档

### Q4: 推送有限制吗？

**免费版限制：**
- 每天最多 5 条推送消息
- 每条消息最大 10KB

对于每日签到来说，完全够用。

### Q5: 如何关闭推送？

在 `config.json` 中设置：
```json
{
  "push": {
    "enabled": false
  }
}
```

## 进阶配置

### 自定义推送内容

如果你想自定义推送内容，可以修改 `main.py` 中的 `send_notification` 函数：

```python
def send_notification(pusher, account_name, result):
    title = "自定义标题"
    content = "自定义内容"
    pusher.send(title, content)
```

### 多消息通道

Server 酱支持配置多个消息通道：
1. 登录 Server 酱后台
2. 进入"消息通道"配置
3. 添加企业微信、钉钉、飞书等通道
4. 配置完成后，推送会同时发送到所有通道

## 相关链接

- [Server 酱官网](https://sct.ftqq.com/)
- [Server 酱文档](https://sct.ftqq.com/docs)
- [消息通道配置](https://sct.ftqq.com/sendkey)

---

如有其他问题，欢迎提交 Issue！
