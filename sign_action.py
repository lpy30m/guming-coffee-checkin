import hashlib
import json
import secrets
import string
import time
import requests


def generate_nonce_str(length=32):
    """生成随机nonceStr"""
    alphabet = string.ascii_letters + string.digits + "-_"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def generate_post_xmsign(data, nonce_str, timestamp, xm_token=""):
    """
    生成POST请求的xmSign

    Args:
        data: 请求body数据（字典）
        nonce_str: 随机字符串
        timestamp: 时间戳（字符串或整数）
        xm_token: token（可选）

    Returns:
        xmSign字符串
    """
    # 密钥
    secret_key = "uh3$Hg&^HK876%gbxVG7f$%p=0M~>s1x"

    # 合并所有参数
    sign_params = {
        **data,  # POST的body数据
        "nonceStr": nonce_str,
        "xmTimestamp": str(timestamp),
        "xmToken": xm_token,
    }
    print(sign_params)

    # 如果有xmToken，也加入签名（根据代码：xmToken在headers中，但可能也在data中）
    # 从代码看：xmToken: e && e.xmToken ? e.xmToken : ""
    # 如果data中有xmToken，会被包含进去

    # 按key排序
    sorted_keys = sorted(sign_params.keys())
    print(sorted_keys)
    # 拼接参数值
    concat_str = ""
    for key in sorted_keys:
        value = sign_params[key]
        if isinstance(value, (dict, list)):
            # 对象类型转JSON字符串（无空格）
            concat_str += json.dumps(value, separators=(",", ":"), ensure_ascii=False)
        else:
            concat_str += str(value)

    # 加密钥后计算MD5
    sign_str = concat_str + secret_key
    print(f"拼接值: {sign_str}")
    xm_sign = hashlib.md5(sign_str.encode("utf-8")).hexdigest()

    return xm_sign


# 原始数据
data = {"patchDate": "2025-12-10"}

xmTimestamp = str(int(time.time() * 1000))
# xmTimestamp = "1765334216111"
xmToken = "8047087969542797917@e62e9a91e3bf76a338abfc45dc3e79a7"
headers = {
    "sec-ch-ua-platform": '"Android"',
    "Referer": "https://p60718618653004equ-saas.yl-activity.meta-xuantan.com/activityMultiport.html?appKey=hdzy_gmkjjt_aeuyur&placeId=6071861865300&activityPlanId=44993818764&applicationId=11&li=0132541916176534842173159328666627901045&hi=xmps&channelType=1050&platformEnv=4&devVersion=DV100&idxgy=89n08qvl&eoq=0dzibt7pk983",
    "xmSign": "cf4a44e82a10ddb06ac1269edb3e020b",
    "sec-ch-ua": '"Chromium";v="142", "Android WebView";v="142", "Not_A Brand";v="99"',
    "sec-ch-ua-mobile": "?1",
    "bdrk": "null",
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; JER-AN20 Build/HUAWEIJER-AN20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/142.0.7444.172 Mobile Safari/537.36 XWEB/1420045 MMWEBSDK/20251006 MMWEBID/8151 MicroMessenger/8.0.66.2980(0x28004234) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 miniProgram/wx1736dcbd36f4c055",
    "ri": "",
    "Content-Type": "application/json",
    "xmToken": xmToken,
    "nonceStr": generate_nonce_str(),
    "xmTimestamp": xmTimestamp,
    "functionId": "0",
}


# headers中的值
nonce_str = headers["nonceStr"]
timestamp = headers["xmTimestamp"]
xm_token = headers["xmToken"]

# 计算签名
xm_sign = generate_post_xmsign(data, nonce_str, timestamp, xm_token)

print(f"用于签名的参数: {sorted(data.keys())}")
print(f"xmSign: {xm_sign}")
headers["xmSign"] = xm_sign

cookies = {
    "loginTime": "hdzy_gmkjjt_aeuyur=1765333388302",
    "userId": "hdzy_gmkjjt_aeuyur=8042474550720305503",
    "ls": "hdzy_gmkjjt_aeuyur=3792248922176533338802059328666694930560-1",
    "appKey": "hdzy_gmkjjt_aeuyur",
    "consumerId": "hdzy_gmkjjt_aeuyur=2000000000602009457",
    "placeId": "hdzy_gmkjjt_aeuyur=6071861865300",
    "openId": "hdzy_gmkjjt_aeuyur=2000000000602009457",
    "unionId": "hdzy_gmkjjt_aeuyur="
}

url = "https://p60718618653004equ-saas.yl-activity.meta-xuantan.com/sign/action"

json_data = {
    "patchDate": "2025-12-10",
}

print(data)
print(headers)
# exit()


response = requests.post(url, headers=headers, cookies=cookies, json=json_data)

print(response.text)
print(response)
