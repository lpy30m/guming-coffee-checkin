# 参数配置重要说明

## ⚠️ 参数对应关系

### 必须成套提取

**关键参数**：`host`、`li`、`idxgy`、`eoq`

> [!WARNING]
> 这四个参数**必须从同一个活动链接中一起提取**，每个账户的这些参数都不同，不能混用！

### 为什么需要对应？

这些参数是微信小程序通过云函数动态生成的，它们之间存在关联关系：
- `host` - 活动服务器域名
- `li` - 用户身份标识（长字符串）
- `idxgy` - 会话标识
- `eoq` - 签名参数

**如果参数不匹配**，服务器会返回错误：
- "页面已变化，请重新进入活动页面"
- "签到失败"
- "参数错误"

### 正确的提取方法

#### 1. 使用抓包工具

**推荐工具**：
- iOS: Charles、Thor
- Android: HttpCanary、Packet Capture

**步骤**：
1. 打开抓包工具
2. 在古茗小程序中打开签到活动页面
3. 查找形如以下的 URL 请求：
   ```
   https://pXXXXXequ-saas.yl-activity.meta-xuantan.com/activityMultiport.html?...
   ```
4. **从这一个 URL 中**提取所有四个参数

#### 2. 完整示例

**抓包得到的 URL**：
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
idxgy=89n08qvl&
eoq=0dzibt7pk983
```

**提取参数**：
- `host` = `p60718618653004equ-saas.yl-activity.meta-xuantan.com`
- `li` = `0132541916176534842173159328666627901045`
- `idxgy` = `89n08qvl`
- `eoq` = `0dzibt7pk983`

**填入配置**：
```json
{
  "account": {
    "name": "我的账号",
    "host": "p60718618653004equ-saas.yl-activity.meta-xuantan.com",
    "li": "0132541916176534842173159328666627901045",
    "idxgy": "89n08qvl",
    "eoq": "0dzibt7pk983",
    "cookies": { /* ... */ }
  }
}
```

### 参数可能会变化

> [!NOTE]
> 这些参数由微信云函数生成，可能会在以下情况变化：
> - 活动页面更新
> - 长时间未访问
> - 账号重新登录
> 
> **如果签到失败**，请重新抓包获取最新的参数！

### 常见错误

❌ **错误做法**：
```json
{
  "account": {
    "host": "从A链接提取的",
    "li": "从B链接提取的",    // ❌ 不同链接
    "idxgy": "从C链接提取的", // ❌ 不同链接
    "eoq": "从D链接提取的"    // ❌ 不同链接
  }
}
```

✅ **正确做法**：
```json
{
  "account": {
    "host": "从同一个链接提取",
    "li": "从同一个链接提取",
    "idxgy": "从同一个链接提取",
    "eoq": "从同一个链接提取"    // ✅ 都来自同一个URL
  }
}
```

### 参数名称可能不同

> [!TIP]
> 不同用户或不同时间的 URL，参数名称可能略有不同（如 `sbs` 代替 `eoq`），但位置和作用相同。
> 
> **请根据实际 URL 调整参数名称**，在配置文件中仍使用标准名称（`li`、`idxgy`、`eoq`）。

### 故障排除

**症状**：签到失败，提示"页面已变化"

**解决方法**：
1. 重新打开古茗小程序签到活动页面
2. 重新抓包获取最新的完整 URL
3. 提取所有四个参数并更新到 `config.json`
4. 重新运行签到程序

---

**总结**：这四个参数就像一套"钥匙"，必须配套使用才能打开签到的"门"！🔑
