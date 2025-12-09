# 企业微信推送配置教程

本教程将指导您如何配置企业微信应用消息推送功能。

## 为什么选择企业微信？

- ✅ **完全免费**：个人也可以注册企业微信，无需企业认证
- ✅ **推送稳定**：官方接口，稳定可靠
- ✅ **配置简单**：只需几分钟即可完成配置
- ✅ **支持多人**：可以推送给多个成员

## 配置步骤

### 1. 注册企业微信

1. 访问 [企业微信官网](https://work.weixin.qq.com/)
2. 点击"立即注册"
3. 选择"其他行业" 或 "IT/互联网"
4. 填写企业信息（可以填写个人信息）
5. 完成注册

### 2. 创建应用

1. 登录企业微信管理后台：https://work.weixin.qq.com/
2. 点击左侧菜单 **应用管理**
3. 点击 **创建应用**
4. 填写应用信息：
   - 应用名称：`古茗签到通知`（或其他名称）
   - 应用 Logo：上传一个图标（可选）
   - 应用介绍：`用于推送古茗签到通知`
5. 点击 **创建应用**

### 3. 获取配置参数

创建完成后，您需要获取三个重要参数：

#### 3.1 获取 CorpID

1. 在管理后台点击 **我的企业**
2. 在页面底部找到 **企业 ID**
3. 复制这个 ID，这就是 `corpid`

#### 3.2 获取 AgentID 和 CorpSecret

1. 点击 **应用管理**
2. 点击刚才创建的应用
3. 在应用详情页面可以看到：
   - **AgentId**：复制这个数字，这就是 `agentid`
   - **Secret**：点击"查看"并复制，这就是 `corpsecret`

### 4. 添加可见范围

1. 在应用详情页面，找到 **可见范围**
2. 点击 **添加成员**
3. 选择需要接收消息的成员（通常选择自己）
4. 保存

### 5. 配置到项目

将获取的参数填入 `config.json`：

```json
{
  "accounts": [
    {
      "phone": "您的手机号",
      "password": "您的密码",
      "name": "主账号"
    }
  ],
  "wechat_push": {
    "enabled": true,
    "corpid": "这里填写您的 CorpID",
    "corpsecret": "这里填写您的 CorpSecret",
    "agentid": 1000002,
    "touser": "@all"
  }
}
```

参数说明：
- `corpid`：企业 ID
- `corpsecret`：应用的 Secret
- `agentid`：应用的 AgentID（数字）
- `touser`：接收消息的成员
  - `@all`：发送给所有成员
  - 指定成员：填写成员 UserID（在"通讯录"中查看）

### 6. 测试推送

运行以下测试代码验证配置是否正确：

```python
from wechat_pusher import WechatPusher

pusher = WechatPusher(
    corpid="您的corpid",
    corpsecret="您的corpsecret",
    agentid=您的agentid,
    touser="@all"
)

pusher.send_text_message("测试通知", "如果您收到这条消息，说明配置成功！")
```

如果配置正确，您将在企业微信中收到消息通知。

## 常见问题

### Q1: 收不到推送消息？

**检查以下几点：**
1. 确认参数填写正确（特别注意 `agentid` 应为数字类型）
2. 确认成员在应用的"可见范围"内
3. 确认企业微信客户端已登录
4. 检查是否有报错信息

### Q2: 提示 "access_token invalid"？

**解决方法：**
- 重新获取 `corpsecret`（每次查看都会刷新）
- 确认 `corpid` 和 `corpsecret` 没有复制错误

### Q3: 可以发送给多个人吗？

**可以！** 有两种方式：
1. 使用 `@all` 发送给所有成员
2. 使用 `user1|user2|user3` 格式指定多个 UserID

### Q4: 如何查看成员的 UserID？

1. 进入企业微信管理后台
2. 点击 **通讯录**
3. 点击成员名称
4. 查看 **帐号** 字段，这就是 UserID

## 进阶配置

### 发送 Markdown 格式消息

可以使用 `send_markdown_message` 方法发送格式化消息：

```python
content = """
# 签到结果通知
> 时间：2025-01-01 08:00:00

**签到统计**
- ✅ 主账号：签到成功
- ✅ 副账号：签到成功

共计：2/2 成功
"""

pusher.send_markdown_message(content)
```

### 自定义推送时间

如果使用 GitHub Actions，可以修改 `.github/workflows/checkin.yml` 中的 cron 表达式：

```yaml
schedule:
  - cron: '0 0 * * *'  # 每天 UTC 0:00 (北京时间 8:00)
```

Cron 表达式格式：`分 时 日 月 星期`

示例：
- `0 0 * * *`：每天 0:00
- `30 1 * * *`：每天 1:30
- `0 0 * * 1`：每周一 0:00

**注意**：GitHub Actions 使用 UTC 时间，需要换算成北京时间（UTC+8）。

## 相关链接

- [企业微信官网](https://work.weixin.qq.com/)
- [企业微信 API 文档](https://developer.work.weixin.qq.com/document/path/90664)
- [Cron 表达式生成器](https://crontab.guru/)

---

如有其他问题，欢迎提交 Issue！
