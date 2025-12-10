# 快速开始指南 🚀

完整的项目设置和 GitHub 发布流程。

## 📋 前置准备

- [x] Python 3.7+
- [x] Git
- [x] GitHub 账号

## 🎯 步骤 1: 准备工作

### 1.1 获取古茗 API 信息

**⚠️ 重要：** 您需要通过抓包获取古茗 App 的真实 API 地址。

推荐工具：
- **iOS**: Charles、Thor、Shadowrocket
- **Android**: HttpCanary、Packet Capture、Charles

需要抓取的接口：
1. **登录接口**：用户登录时的请求
2. **签到接口**：点击签到时的请求

抓包后需要修改 `checkin.py` 中的：
- `login_url`：登录 API 地址
- `checkin_url`：签到 API 地址
- 请求参数格式（根据实际抓包结果调整）

### 1.2 配置 Server 酱（可选但推荐）

参考 [Server 酱配置教程](docs/server-setup.md) 获取 SendKey。

## 🎯 步骤 2: 本地配置

### 2.1 安装依赖

```bash
pip install -r requirements.txt
```

### 2.2 创建配置文件

```bash
cp config.example.json config.json
```

编辑 `config.json`，填入您的信息：

```json
{
  "accounts": [
    {
      "phone": "您的手机号",
      "password": "您的密码",
      "name": "主账号"
    }
  ],
  "push": {
    "enabled": true,
    "sendkey": "your_sendkey_here"
  }
}
```

### 2.3 本地测试

```bash
python main.py
```

如果看到签到成功的消息，说明配置正确！

## 🎯 步骤 3: 发布到 GitHub

### 3.1 在 GitHub 创建仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `guming-coffee-checkin`
   - **Description**: `古茗咖啡新年签到计划 - 自动签到脚本`
   - **Public**: 选择公开
   - **不要** 勾选 "Initialize this repository with a README"

3. 点击 "Create repository"

### 3.2 推送代码到 GitHub

在项目目录下执行：

```bash
# 添加所有文件（config.json 会被 .gitignore 自动忽略）
git add .

# 提交代码
git commit -m "🎉 Initial commit: 古茗咖啡新年签到计划"

# 添加远程仓库（替换成您的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/guming-coffee-checkin.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 3.3 配置 GitHub Secrets（用于自动化）

1. 进入您的 GitHub 仓库页面
2. 点击 **Settings** > **Secrets and variables** > **Actions**
3. 点击 **New repository secret**
4. 添加名为 `CONFIG_JSON` 的 Secret
5. 值为您的 `config.json` 文件的完整内容
6. 点击 **Add secret**

### 3.4 启用 GitHub Actions

1. 进入仓库的 **Actions** 标签页
2. 点击 **I understand my workflows, go ahead and enable them**
3. 找到 "古茗咖啡每日签到" 工作流
4. 点击 **Enable workflow**

### 3.5 测试 GitHub Actions

点击 **Run workflow** > **Run workflow** 手动触发一次，验证是否正常工作。

## 🎯 步骤 4: 享受自动化

✅ 完成！现在每天早上 8:00，GitHub Actions 会自动执行签到任务，并通过微信推送通知您！

## 📱 推送效果示例

签到成功后，您将收到类似这样的微信消息：

```
🎉 古茗签到结果通知

📊 签到统计: 1/1 成功
⏰ 时间: 2025-01-01 08:00:00

详细结果:
✅ 主账号: 签到成功！获得 10 积分，已连续签到 5 天
```

## 🔧 自定义配置

### 修改签到时间

编辑 `.github/workflows/checkin.yml`：

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 0:00 = 北京时间 8:00
```

改为其他时间，例如晚上 8:00（UTC 12:00）：

```yaml
schedule:
  - cron: '0 12 * * *'
```

### 添加多个账户

在 `config.json` 的 `accounts` 数组中添加：

```json
{
  "accounts": [
    {
      "phone": "13800138000",
      "password": "password1",
      "name": "主账号"
    },
    {
      "phone": "13800138001",
      "password": "password2",
      "name": "副账号"
    }
  ]
}
```

## 🆘 遇到问题？

### 问题 1: GitHub Actions 运行失败

- 检查 `CONFIG_JSON` Secret 是否正确配置
- 查看 Actions 运行日志，找到具体错误信息

### 问题 2: 签到失败

- 确认账号密码正确
- 检查 API 地址是否正确（需要抓包验证）
- 查看报错信息

### 问题 3: 微信推送失败

- 参考 [Server 酱配置教程](docs/server-setup.md)
- 确认三个参数填写正确
- 测试 access_token 是否能正常获取

## 📚 更多文档

- [Server 酱配置教程](docs/server-setup.md)
- [README.md](README.md)

---

🎉 祝您使用愉快！有问题欢迎提 Issue！
