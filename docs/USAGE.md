# 古茗咖啡新年签到 - 使用说明

## 快速上手

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置账户信息

复制示例配置文件：

```bash
cp config.example.json config.json
```

编辑 `config.json`，填入您的信息：

```json
{
  "account": {
    "name": "我的账号",
    "li": "您的li参数",
    "eoq": "您的eoq参数",
    "cookies": {
      "loginTime": "hdzy_gmkjjt_aeuyur=...",
      "userId": "hdzy_gmkjjt_aeuyur=...",
      "ls": "hdzy_gmkjjt_aeuyur=...",
      "appKey": "hdzy_gmkjjt_aeuyur",
      "consumerId": "hdzy_gmkjjt_aeuyur=...",
      "placeId": "hdzy_gmkjjt_aeuyur=6071861865300",
      "openId": "hdzy_gmkjjt_aeuyur=...",
      "unionId": "hdzy_gmkjjt_aeuyur="
    }
  }
}
```

### 3. 运行签到

```bash
python main.py
```

## 参数获取详细教程

### 📌 获取 li 和 eoq 参数

这两个参数来自古茗活动页面的 URL。

**方法一：通过抓包工具（推荐）**

1. 使用抓包工具（如 Charles、HttpCanary）
2. 打开古茗小程序，进入新年签到活动页面
3. 查看网络请求中的活动页面 URL
4. 找到形如以下格式的 URL：

```
https://p60718618653004equ-saas.yl-activity.meta-xuantan.com/activityMultiport.html?
appKey=hdzy_gmkjjt_aeuyur&
placeId=6071861865300&
activityPlanId=44993818764&
applicationId=11&
li=0132541916176534842173159328666627901045&
hi=xmps&
channelType=1050&
platformEnv=4&
devVersion=DV100&
eoq=0dzibt7pk983
```

5. 提取参数：
   - `li` = `0132541916176534842173159328666627901045`
   - `eoq` = `0dzibt7pk983`

**方法二：通过浏览器开发者工具**

1. 如果您能在浏览器中访问活动页面
2. 按 F12 打开开发者工具
3. 切换到 Network（网络）标签
4. 刷新页面
5. 查找活动页面的请求，从 URL 中提取 `li` 和 `eoq`

### 🍪 获取 Cookie 信息

**方法一：抓包工具（推荐）**

1. 打开抓包工具（Charles、HttpCanary 等）
2. 在古茗小程序中登录您的账号
3. 进入新年签到活动页面
4. 查看任意一个请求的 Cookie 信息
5. 复制以下字段的值：
   - `loginTime`
   - `userId`
   - `ls`
   - `appKey`
   - `consumerId`
   - `placeId`
   - `openId`
   - `unionId`

**Cookie 示例**：

```
loginTime: hdzy_gmkjjt_aeuyur=1765333388302
userId: hdzy_gmkjjt_aeuyur=8042474550720305503
ls: hdzy_gmkjjt_aeuyur=3792248922176533338802059328666694930560-1
appKey: hdzy_gmkjjt_aeuyur
consumerId: hdzy_gmkjjt_aeuyur=2000000000602009457
placeId: hdzy_gmkjjt_aeuyur=6071861865300
openId: hdzy_gmkjjt_aeuyur=2000000000602009457
unionId: hdzy_gmkjjt_aeuyur=
```

将这些值填入 `config.json` 中。

## 签到流程说明

程序会自动执行三个步骤：

1. **步骤1: 获取基础参数**
   - 发送基础参数请求
   - 验证账号有效性

2. **步骤2: 获取用户 Token**
   - 获取临时 Token（xmToken）
   - 用于后续签到请求

3. **步骤3: 执行签到**
   - 使用 Token 提交签到请求
   - 检查返回结果中的 `desc` 字段
   - `desc` 为 "成功" 表示签到成功

## 运行结果说明

### 成功签到

```
==================================================
🎉 古茗咖啡新年签到计划 🎉
==================================================
⏰ 执行时间: 2025-12-10 14:00:00

✅ 微信推送模块已启用

🎯 开始签到: 我的账号
==================================================
📝 步骤1: 获取基础参数...
✅ 步骤1完成: 基础参数请求成功
📝 步骤2: 获取用户 Token...
✅ 步骤2完成: 获取 Token 成功
📝 步骤3: 执行签到...
✅ 签到成功！日期: 2025-12-10
==================================================

✅ 微信推送发送成功！

============================================================
✨ 签到完成！
============================================================
```

### 已签到过

```
📝 步骤3: 执行签到...
ℹ️  今日已签到
```

### Cookie 失效

```
❌ 步骤1失败: ...
❌ 步骤2失败: ...
```

**解决方法**：重新获取 Cookie 并更新 `config.json`

## 常见问题

### Q1: 如何获取 li 和 eoq 参数？

A: 这两个参数在活动页面 URL 中，使用抓包工具可以看到。参考上方"参数获取详细教程"。

### Q2: Cookie 有效期多久？

A: Cookie 有效期不固定，通常几天到几周不等。失效后需要重新获取。

### Q3: 可以同时签到多个账号吗？

A: 当前版本仅支持单账户签到。多账户支持将在后续版本中添加。

### Q4: 签到时间可以自定义吗？

A: 可以。如果使用 GitHub Actions，可以修改 `.github/workflows/checkin.yml` 中的 cron 表达式。

### Q5: 微信推送是必须的吗？

A: 不是。如果不需要微信推送，可以在 `config.json` 中设置 `"enabled": false`。

## 自动化签到（GitHub Actions）

### 配置步骤

1. Fork 本仓库到您的 GitHub 账号

2. 进入仓库的 **Settings** > **Secrets and variables** > **Actions**

3. 点击 **New repository secret**

4. 添加 Secret：
   - Name: `CONFIG_JSON`
   - Value: 您的完整 `config.json` 内容

5. 进入 **Actions** 标签页，启用工作流

6. 脚本将在每天早上 8:00 (UTC+8) 自动运行

### 手动触发

进入 **Actions** 标签页，选择工作流，点击 **Run workflow** 手动触发。

## 安全提醒

⚠️ **重要**：
- 请勿将 `config.json` 提交到 Git 仓库
- Cookie 包含敏感信息，请妥善保管
- 建议定期更新 Cookie
- 使用 GitHub Actions 时，配置信息存储在 Secret 中，相对安全

## 技术说明

### 签名算法

程序实现了三种签名算法：

1. **GET 请求签名**：参数按字典序排序后拼接，加密钥后 MD5
2. **Token 签名**：li + nonceStr + timestamp + 固定密钥的 MD5
3. **POST 请求签名**：body + nonceStr + xmTimestamp + xmToken 排序拼接后加密钥 MD5

### 请求流程

```
用户 → [步骤1] getBaseParams → 验证账号
    → [步骤2] getUserToken → 获取 xmToken  
    → [步骤3] sign/action → 提交签到
```

每个步骤都需要正确的签名才能通过验证。

---

如有问题，欢迎提 Issue！
