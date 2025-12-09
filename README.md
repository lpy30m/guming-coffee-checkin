# 古茗咖啡新年签到计划 🎉☕

Guming Coffee New Year Check-in Plan - 自动签到脚本，支持微信推送通知

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 项目简介

这是一个自动化签到脚本，用于古茗咖啡的新年签到活动。签到成功后会通过微信推送通知您。

## 功能特性

- ✅ 自动完成每日签到
- 📱 签到成功后微信推送通知
- ⏰ 支持定时任务（配合 GitHub Actions 或 Cron）
- 🔐 安全的配置文件管理
- 📊 签到日志记录

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
  "accounts": [
    {
      "phone": "您的手机号",
      "password": "您的密码",
      "name": "账户备注名"
    }
  ],
  "wechat_push": {
    "corpid": "企业微信 CorpID",
    "corpsecret": "企业微信 CorpSecret",
    "agentid": "应用 AgentID",
    "touser": "@all"
  }
}
```

### 4. 运行脚本

```bash
python main.py
```

## 微信推送配置

本项目使用企业微信应用消息推送，您需要：

1. 注册企业微信（免费）：https://work.weixin.qq.com/
2. 创建应用获取 `CorpID`、`CorpSecret` 和 `AgentID`

详细教程请参考：[企业微信应用消息推送配置教程](docs/wechat-setup.md)

## GitHub Actions 自动化

项目已配置 GitHub Actions，可以每天自动执行签到任务。

### 设置步骤：

1. Fork 本仓库
2. 在仓库的 Settings > Secrets and variables > Actions 中添加以下 Secrets：
   - `CONFIG_JSON`：您的完整 config.json 内容

3. 启用 Actions：在 Actions 标签页中启用工作流

脚本将在每天早上 8:00 (UTC+8) 自动运行。

## 项目结构

```
.
├── main.py                 # 主程序入口
├── checkin.py             # 签到核心逻辑
├── wechat_pusher.py       # 微信推送模块
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
A: 请检查企业微信配置是否正确，确保 CorpID、CorpSecret 和 AgentID 填写无误。

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
