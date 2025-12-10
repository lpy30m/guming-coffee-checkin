# GitHub 发布指南

## 📦 推送到 GitHub

### 方法一：通过命令行推送（推荐）

#### 1. 在 GitHub 创建仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `guming-coffee-checkin`（或您喜欢的名称）
   - **Description**: `古茗咖啡新年签到计划 - 自动签到脚本，支持 Server 酱推送`
   - **Public**: 选择公开（如果要分享给其他人）
   - **不要** 勾选 "Initialize this repository with a README"（因为本地已有）
3. 点击 "Create repository"

#### 2. 推送代码

在项目目录执行以下命令：

```bash
# 添加远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/guming-coffee-checkin.git

# 设置主分支
git branch -M main

# 推送到 GitHub
git push -u origin main
```

**示例**：
```bash
# 如果你的 GitHub 用户名是 zhangsan
git remote add origin https://github.com/zhangsan/guming-coffee-checkin.git
git branch -M main
git push -u origin main
```

#### 3. 验证推送

推送成功后，访问 `https://github.com/YOUR_USERNAME/guming-coffee-checkin` 查看仓库。

### 方法二：使用 GitHub Desktop

1. 下载并安装 GitHub Desktop: https://desktop.github.com/
2. 打开 GitHub Desktop
3. 点击 "File" > "Add Local Repository"
4. 选择项目文件夹: `/Users/jiangxia/code/古茗/签到活动`
5. 点击 "Publish repository"
6. 填写仓库名称和描述，点击 "Publish Repository"

---

## 🔐 配置 GitHub Secrets（用于自动化）

### 为什么需要 Secrets？

GitHub Actions 需要读取配置文件才能自动签到，但配置文件包含敏感信息（cookies、sendkey），不能直接提交到仓库。

### 配置步骤

1. **进入仓库 Settings**
   - 访问你的仓库页面
   - 点击页面上方的 "Settings"

2. **添加 Secret**
   - 左侧菜单选择 "Secrets and variables" > "Actions"
   - 点击 "New repository secret"

3. **添加 CONFIG_JSON**
   - Name: `CONFIG_JSON`
   - Secret: 粘贴你的 `config.json` 完整内容
   - 点击 "Add secret"

**config.json 示例**：
```json
{
  "account": {
    "name": "主账号",
    "host": "p60718618653004equ-saas.yl-activity.meta-xuantan.com",
    "li": "你的li参数",
    "idxgy": "你的idxgy参数",
    "eoq": "你的eoq参数",
    "cookies": { ... }
  },
  "push": {
    "enabled": true,
    "sendkey": "你的Server酱SendKey"
  }
}
```

4. **启用 GitHub Actions**
   - 点击仓库页面上方的 "Actions"
   - 如果看到提示，点击 "I understand my workflows, go ahead and enable them"

5. **测试运行**
   - 进入 Actions 标签页
   - 选择 "古茗咖啡每日签到" 工作流
   - 点击 "Run workflow" > "Run workflow"
   - 等待运行完成，查看日志

---

## ⏰ 设置自动化签到时间

默认配置是每天早上 8:00 (北京时间) 自动签到。

### 修改签到时间

编辑 `.github/workflows/checkin.yml`：

```yaml
on:
  schedule:
    # 每天早上 8:00 (UTC+8 = UTC 0:00) 自动执行
    - cron: '0 0 * * *'
```

**时间对照表**：
- `0 0 * * *` - 每天 0:00 UTC (北京时间 8:00)
- `0 12 * * *` - 每天 12:00 UTC (北京时间 20:00)
- `30 1 * * *` - 每天 1:30 UTC (北京时间 9:30)

> **注意**：GitHub Actions 使用 UTC 时间，需要减去 8 小时换算。

---

## 📊 查看运行日志

1. 进入仓库的 "Actions" 标签页
2. 点击具体的运行记录
3. 查看 "执行签到" 步骤的日志

**成功的日志示例**：
```
🎉 古茗咖啡新年签到计划 🎉
⏰ 执行时间: 2025-12-10 16:32:03
✅ Server 酱推送模块已启用
🎯 开始签到: 主账号
📝 步骤1: 获取基础参数...
✅ 步骤1完成: 基础参数请求成功
📝 步骤2: 获取用户 Token...
✅ 步骤2完成: 获取 Token 成功
📝 步骤3: 执行签到...
ℹ️  今日已签到
✅ 推送发送成功！
✨ 签到完成！
```

---

## 🎯 完成清单

推送到 GitHub 后，确保完成以下任务：

- [ ] 仓库已创建并推送成功
- [ ] 添加了 `CONFIG_JSON` Secret
- [ ] 启用了 GitHub Actions
- [ ] 手动测试运行成功
- [ ] 收到了 Server 酱推送通知
- [ ] 修改 README.md 中的仓库链接（如需要）

---

## 常见问题

### Q1: 推送时提示权限错误？

**错误信息**：
```
remote: Permission to xxx/xxx.git denied
```

**解决方法**：
1. 配置 GitHub 认证：
   ```bash
   git config --global user.name "你的用户名"
   git config --global user.email "你的邮箱"
   ```
2. 使用 Personal Access Token 代替密码
   - 访问 https://github.com/settings/tokens
   - 生成新的 token
   - 推送时使用 token 作为密码

### Q2: GitHub Actions 运行失败？

**检查项**：
1. CONFIG_JSON Secret 是否正确配置
2. JSON 格式是否正确（可用 https://jsonlint.com/ 验证）
3. Actions 是否已启用
4. 查看具体的错误日志

### Q3: 自动签到不触发？

**可能原因**：
1. GitHub Actions 可能有延迟（最多几分钟）
2. 检查 cron 表达式是否正确
3. 确认工作流文件路径正确：`.github/workflows/checkin.yml`

---

## 🎉 完成！

现在你的古茗签到项目已经推送到 GitHub，并配置了自动化签到！

每天会自动执行签到，并通过 Server 酱推送结果到您的微信。

**项目链接**：`https://github.com/YOUR_USERNAME/guming-coffee-checkin`

---

**祝签到愉快！**☕🎊
