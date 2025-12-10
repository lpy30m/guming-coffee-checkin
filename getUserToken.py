import hashlib
import base64
import json
import time
import requests
import secrets

def generate_nonce_str_exact(length=32):
    """
    精确模拟原JS代码的nonceStr生成逻辑
    """
    random_bytes = secrets.token_bytes(length)
    result = ""
    
    for byte in random_bytes:
        # 取低6位 (byte & 63)
        t = byte & 63
        
        if t < 36:
            # 0-35: 转为36进制 (0-9a-z)
            result += str(t) if t < 10 else chr(ord('a') + t - 10)
        elif t < 62:
            # 36-61: 转为大写字母 (A-Z)
            result += chr(ord('A') + t - 36)
        elif t == 62:
            result += "-"
        else:  # t == 63
            result += "_"
    
    return result


def md5(text):
    return hashlib.md5(text.encode()).hexdigest()


# 密钥
secret_key = base64.b64decode("dWgzJEhnJl5ISzg3NiVnYnhWRzdmJCVwPTBNfj5zMXg=").decode(
    "utf-8"
)
# 结果: uh3$Hg^HK876%gbxVG7f$%p=0M~>s1x
xmTimestamp = str(int(time.time() * 1000))


headers = {
    "Host": "p6071861865300hc04-saas.yl-activity.meta-xuantan.com",
    "Connection": "keep-alive",
    "xmSign": "",
    "xmTimestamp": xmTimestamp,
    "xmToken": "",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.8(0x13080813) XWEB/1227",
    "bdrk": "null",
    "nonceStr": generate_nonce_str_exact(),
    "ri": "",
    "functionId": "0",
    "Accept": "*/*",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://p60718618653004equ-saas.yl-activity.meta-xuantan.com/activityMultiport.html?appKey=hdzy_gmkjjt_aeuyur&placeId=6071861865300&activityPlanId=44993818764&applicationId=11&li=0132541916176534842173159328666627901045&hi=xmps&channelType=1050&platformEnv=4&devVersion=DV100&idxgy=89n08qvl&eoq=0dzibt7pk983",   
    "Accept-Language": "zh-CN,zh;q=0.9"
}

# URL参数（从你的params）
params = {
    "timestamp": xmTimestamp,
    "nonceStr": generate_nonce_str_exact(),
    "tokenSign": ""
}
params["tokenSign"] = md5(
    "0132541916176534842173159328666627901045" # params中的li 
    + params["nonceStr"]
    + params["timestamp"]
    + "J7h8&^Bgs5#bn*7hn%!=kh308*bv2!s^"
)
print(f"tokenSign: {params['tokenSign']}")


# ============== 签名计算（使用临时字典）==============
# 创建一个临时字典用于签名计算，不影响原params
sign_params = {
    **params,  # 复制原params的所有内容
    "nonceStr": headers['nonceStr'],  # 用headers中的nonceStr覆盖
    "xmTimestamp": xmTimestamp,  # 添加xmTimestamp
    # "xmToken": ""  # 如果有xmToken，也加入
}

print(f"用于签名的参数: {sign_params}")

# 按key排序
sorted_keys = sorted(sign_params.keys())

# 拼接参数值
concat_str = ""
for key in sorted_keys:
    value = sign_params[key]
    if isinstance(value, dict):
        concat_str += json.dumps(value, separators=(",", ":"))
    else:
        concat_str += str(value)

print(f"排序后的keys: {sorted_keys}")
print(f"拼接字符串: {concat_str}")

# 加密钥后计算MD5
sign_str = concat_str + secret_key
print(f"签名原文: {sign_str}")

xmSign = hashlib.md5(sign_str.encode("utf-8")).hexdigest()
headers["xmSign"] = xmSign

print(f"\nxmSign: {xmSign}")

# cookies = {
#     "loginTime": "hdzy_gmkjjt_aeuyur=1765279658911",
#     "userId": "hdzy_gmkjjt_aeuyur=943517868434632393",
#     "ls": "hdzy_gmkjjt_aeuyur=6728655998176527965877275481656629677658-1",
#     "appKey": "hdzy_gmkjjt_aeuyur",
#     "consumerId": "hdzy_gmkjjt_aeuyur=1593914291513282561",
#     "placeId": "hdzy_gmkjjt_aeuyur=6071861865300",
#     "openId": "hdzy_gmkjjt_aeuyur=1593914291513282561",
#     "unionId": "hdzy_gmkjjt_aeuyur=",
#     "reloadNum": "\"0\""
# }

# cookies = {
#     "loginTime": "hdzy_gmkjjt_aeuyur=1765333388302",
#     "userId": "hdzy_gmkjjt_aeuyur=8042474550720305503",
#     "ls": "hdzy_gmkjjt_aeuyur=0132541916176534842173159328666627901045-1",
#     "appKey": "hdzy_gmkjjt_aeuyur",
#     "consumerId": "hdzy_gmkjjt_aeuyur=2000000000602009457",
#     "placeId": "hdzy_gmkjjt_aeuyur=6071861865300",
#     "openId": "hdzy_gmkjjt_aeuyur=2000000000602009457",
#     "unionId": "hdzy_gmkjjt_aeuyur="
# }

# url = "https://p6071861865300hc04-saas.yl-activity.meta-xuantan.com/xm/token/getUserToken"

url = "https://p60718618653004equ-saas.yl-activity.meta-xuantan.com/xm/token/getUserToken"

response = requests.get(url, headers=headers,  params=params).json()

print(response)
# {"code":"0","desc":"成功","data":"943517868434632393@02d24baed622e01ed770e425b8014f76"}
xmtoken = response['data']
print(xmtoken)