# 古茗咖啡新年签到计划 🎉☕

Guming Coffee New Year Check-in Plan - 自动签到脚本，支持微信推送通知

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 项目简介

这是一个自动化签到脚本，用于古茗咖啡的新年签到活动。签到成功后会通过微信推送通知您。

## 功能特性

- ✅ 自动完成每日签到（三步签到流程）
- 📱 签到成功后微信推送通知
- ⏰ 支持定时任务（配合 GitHub Actions 或 Cron）
- 🔐 安全的配置文件管理
- 📊 签到日志记录

> **注意**：当前版本仅支持单账户签到

## 快速开始

### 1. 环境要求

- Python 3.7+
- pip

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置文件

复制 `config.example.json` 为 `config.json` 并填入您的信息：

```bash
cp config.example.json config.json
```

编辑 `config.json`：

```json
{
  "account": {
    "name": "账户备注名",
    "host": "p60718618653004equ-saas.yl-activity.meta-xuantan.com",
    "li": "从活动链接中提取的 li 参数",
    "url_params": {
      "idxgy": "从活动链接中提取的参数值",
      "eoq": "从活动链接中提取的参数值"
    },
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
  },
  "push": {
    "enabled": true,
    "sendkey": "您的 Server 酱 SendKey"
  }
}
```

### 4. 运行脚本

```bash
python main.py
```

## 参数获取方法

> [!WARNING]
> **非常重要**：`host`、`li` 和 `url_params` 中的所有参数必须从同一个活动链接中成套提取，否则签到会失败！

> [!NOTE]
> 这些参数可能在微信小程序中通过云函数生成，每次打开活动页面时可能会变化。如果签到失败提示"页面已变化"，请重新获取最新的参数。

### 获取 host 参数

`host` 是活动页面的域名，从完整的活动链接 URL 中提取。

**示例 URL**：
```
https://p60718618653004equ-saas.yl-activity.meta-xuantan.com/activityMultiport.html?...
```

提取域名部分：
- `host` = `p60718618653004equ-saas.yl-activity.meta-xuantan.com`

> **注意**：不同用户的 host 可能不同，请根据您实际的活动链接填写。

### 获取 li 和 url_params 参数

> [!IMPORTANT]
> URL 中的参数名称可能不固定（如 `idxgy`/`ujdnf`、`eoq`/`sbs` 等），请根据实际 URL 配置！

1. 打开古茗小程序活动页面
2. 使用抓包工具（Charles、HttpCanary 等）查看完整的活动链接 URL
3. 从 URL 中成套提取参数

**示例 URL 1**：
```
https://p60718618653004equ-saas.yl-activity.meta-xuantan.com/activityMultiport.html?
appKey=hdzy_gmkjjt_aeuyur&placeId=6071861865300&activityPlanId=44993818764&
applicationId=11&li=0132541916176534842173159328666627901045&hi=xmps&
channelType=1050&platformEnv=4&devVersion=DV100&idxgy=89n08qvl&eoq=0dzibt7pk983
```
在checkin.py中 主要对比是你的self.page_url,可能你获取到的链接中,不一定是idxgy 和 eoq，可能需要手动更改了。

从上述 URL 中提取：
- `host` = `p60718618653004equ-saas.yl-activity.meta-xuantan.com`
- `li` = `0132541916176534842173159328666627901045`
- `url_params` = `{"idxgy": "89n08qvl", "eoq": "0dzibt7pk983"}`

**示例 URL 2** (不同的参数名):
```
https://p60718618653004equ-saas.yl-activity.meta-xuantan.com/activityMultiport.html?
appKey=hdzy_gmkjjt_aeuyur&placeId=6071861865300&
li=3792248922176533338802059328666694930560&
ujdnf=7omaga1t&sbs=qn6tg1nsvoh0
```

从上述 URL 中提取：
- `host` = `p60718618653004equ-saas.yl-activity.meta-xuantan.com`
- `li` = `3792248922176533338802059328666694930560`
- `url_params` = `{"ujdnf": "7omaga1t", "sbs": "qn6tg1nsvoh0"}`

**配置到 config.json**：
```json
{
  "account": {
    "host": "p60718618653004equ-saas.yl-activity.meta-xuantan.com",
    "li": "0132541916176534842173159328666627901045",
    "url_params": {
      "idxgy": "89n08qvl",
      "eoq": "0dzibt7pk983"
    }
  }
}
```

> [!TIP]
> 详细的参数配置说明请查看：[docs/URL_PARAMS.md](docs/URL_PARAMS.md)

### 获取 Cookie

## Cookie 获取方法

### 方法一：抓包工具（推荐）

1. 使用抓包工具（Charles、HttpCanary 等）
2. 打开古茗 App 并登录
3. 在请求中找到 Cookie 字段
4. 复制所需的 Cookie 值到配置文件

### 方法二：浏览器开发者工具

1. 在浏览器中打开古茗活动页面并登录
2. 按 F12 打开开发者工具
3. 切换到 Application/存储 标签
4. 查看 Cookies 并复制所需值

**重要提示**：Cookie 有效期有限，失效后需要重新获取。

## 微信推送配置

本项目使用 [Server酱消息推送](https://sct.ftqq.com/)，您只需要简单访问文档，在`config.json`中配置您的`sendkey`既可

## GitHub Actions 自动化

项目已配置 GitHub Actions，可以每天自动执行签到任务。

### 设置步骤：

1. Fork 本仓库
2. 在仓库的 Settings > Secrets and variables > Actions 中添加以下 Secrets：
   - `CONFIG_JSON`：您的完整 config.json 内容

3. 启用 Actions：在 Actions 标签页中启用工作流

脚本将在每天早上 8:00 (UTC+8) 自动运行。

## 项目结构
docs的文档均为谷歌反重力自动生成，如遇到问题，可在issue中提出。
```
.
├── main.py                 # 主程序入口
├── checkin.py             # 签到核心逻辑
├── server_pusher.py       # 微信推送模块
├── config.example.json    # 配置文件示例
├── config.json            # 配置文件（需自行创建）
├── requirements.txt       # Python 依赖
├── .gitignore            # Git 忽略文件
├── .github/
│   └── workflows/
│       └── checkin.yml   # GitHub Actions 工作流
└── docs/
    └── wechat-setup.md   # 微信推送配置教程
```

## 注意事项

⚠️ **安全提醒**：
- 请勿将 `config.json` 提交到 Git 仓库
- 使用 GitHub Secrets 存储敏感信息
- 定期更改密码以保证账户安全

## 常见问题

### Q: 如何查看签到日志？
A: 日志会输出到控制台，您也可以在 GitHub Actions 的运行记录中查看。

### Q: 可以添加多个账户吗？
A: 可以，在 `config.json` 的 `accounts` 数组中添加多个账户信息即可。

### Q: 微信推送失败怎么办？
A: 请检查Server酱配置是否正确，确保 sendkey 填写无误。

## 开发计划

- [ ] 支持更多推送渠道（钉钉、飞书等）
- [ ] 添加签到失败重试机制
- [ ] Web 界面配置
- [ ] 签到数据统计

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

[MIT License](LICENSE)

## 免责声明

本项目仅供学习交流使用，请勿用于任何商业用途。使用本项目所造成的一切后果由使用者自行承担。

---

⭐ 如果这个项目对您有帮助，欢迎 Star！
