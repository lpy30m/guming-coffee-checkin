# URL 参数配置说明

## 📌 灵活的参数配置

从您的活动链接 URL 中提取参数时，参数名称可能因用户而异。本项目支持**动态配置参数名称**。

## 配置示例

### 示例 1: 标准参数（idxgy + eoq）

**活动 URL**：
```
https://p60718618653004equ-saas.yl-activity.meta-xuantan.com/activityMultiport.html?
appKey=hdzy_gmkjjt_aeuyur&placeId=6071861865300&
li=0132541916176534842173159328666627901045&
idxgy=89n08qvl&eoq=0dzibt7pk983
```

**配置**：
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

### 示例 2: 自定义参数（ujdnf + sbs）

**活动 URL**：
```
https://p60718618653004equ-saas.yl-activity.meta-xuantan.com/activityMultiport.html?
appKey=hdzy_gmkjjt_aeuyur&placeId=6071861865300&
li=3792248922176533338802059328666694930560&
ujdnf=7omaga1t&sbs=qn6tg1nsvoh0
```

**配置**：
```json
{
  "account": {
    "host": "p60718618653004equ-saas.yl-activity.meta-xuantan.com",
    "li": "3792248922176533338802059328666694930560",
    "url_params": {
      "ujdnf": "7omaga1t",
      "sbs": "qn6tg1nsvoh0"
    }
  }
}
```

### 示例 3: 更多参数

如果您的 URL 有更多参数，都可以添加到 `url_params` 中：

```json
{
  "account": {
    "host": "your-host.com",
    "li": "your-li-value",
    "url_params": {
      "param1": "value1",
      "param2": "value2",
      "param3": "value3"
    }
  }
}
```

## ⚙️ 工作原理

程序会自动将 `url_params` 中的所有键值对转换为 URL 参数：

```python
# url_params = {"idxgy": "89n08qvl", "eoq": "0dzibt7pk983"}
# 转换为: idxgy=89n08qvl&eoq=0dzibt7pk983

# url_params = {"ujdnf": "7omaga1t", "sbs": "qn6tg1nsvoh0"}
# 转换为: ujdnf=7omaga1t&sbs=qn6tg1nsvoh0
```

## 🔍 如何提取参数

1. **抓包获取完整 URL**
2. **找到 URL 中固定部分之后的参数**

固定部分：
```
devVersion=DV100
```

固定部分**之后**的所有参数，都应该添加到 `url_params` 中。

**示例分析**：

```
https://host/activityMultiport.html?
appKey=...&placeId=...&li=...&
devVersion=DV100&
idxgy=89n08qvl&    ← 这个加入 url_params
eoq=0dzibt7pk983    ← 这个加入 url_params
```

```json
{
  "url_params": {
    "idxgy": "89n08qvl",
    "eoq": "0dzibt7pk983"
  }
}
```

## ⚠️ 重要提示

> **参数顺序**
> 
> `url_params` 中的参数顺序会按照您在 JSON 中定义的顺序拼接到 URL 中。
> 
> 通常顺序不重要，但如果遇到问题，请尝试调整顺序。

> **参数完整性**
> 
> 确保所有参数都从**同一个 URL** 中提取，不要混用不同链接的参数！

## 💡 常见问题

### Q: 我的 URL 没有 idxgy 怎么办？

A: 没关系！在 `url_params` 中使用您实际 URL 中的参数名即可。

### Q: 我有3个参数怎么办？

A: 在 `url_params` 中添加所有参数：
```json
{
  "url_params": {
    "param1": "value1",
    "param2": "value2",
    "param3": "value3"
  }
}
```

### Q: 参数名称会变化吗？

A: 可能会。如果签到失败，尝试重新抓包获取最新的 URL 和参数。

---

**总结**：`url_params` 让配置更灵活，无论您的 URL 参数叫什么名字，都可以正常使用！🎉
