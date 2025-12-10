import base64
import hashlib
import time
import requests

# getBaseParams 接口
def obj_key_sort(data: dict) -> dict:
    """
    按 key 进行字典序排序
    """
    return dict(sorted(data.items(), key=lambda x: x[0]))


def build_b_string(params: dict) -> str:
    """
    将排序后的字典的所有 value 依序拼接
    """
    s = ""
    for k, v in params.items():
        if isinstance(v, dict):
            # JS 中使用 c.default(i[w])，本质是 JSON.stringify
            import json
            s += json.dumps(v, separators=(',', ':'))
        else:
            s += str(v)
    return s


def build_xm_sign(params: dict) -> str:
    """
    模拟 JS 的 xmSign 生成逻辑
    """
    # 1. 排序
    sorted_params = obj_key_sort(params)

    # 2. 生成 b 值（拼接 value）
    b = build_b_string(sorted_params)

    # 3. Base64 密钥（JS 固定密钥）
    base64_secret = "dWgzJEhnJl5ISzg3NiVnYnhWRzdmJCVwPTBNfj5zMXg="

    # JS: Base64.parse(...).toString(Utf8)
    secret_bytes = base64.b64decode(base64_secret)
    secret_str = secret_bytes.decode("utf-8")

    # 4. 拼接 b + secret 后做 MD5
    sign_input = (b + secret_str).encode("utf-8")
    md5_val = hashlib.md5(sign_input).hexdigest()

    return md5_val


xmTimestamp = str(int(time.time() * 1000))

params = {
    "pageUrl": "https://p60718618653004equ-saas.yl-activity.meta-xuantan.com/activityMultiport.html?appKey=hdzy_gmkjjt_aeuyur&placeId=6071861865300&activityPlanId=44993818764&applicationId=11&li=0132541916176534842173159328666627901045&hi=xmps&channelType=1050&platformEnv=4&devVersion=DV100&idxgy=89n08qvl&eoq=0dzibt7pk983",
    "nonceStr": "69e47daadf2d78aaabd5ff9b1441ded2",
    "xmTimestamp": xmTimestamp
}

xmSign = build_xm_sign(params)
print("xmSign =", xmSign)

headers = {
    "Accept": "application/json",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Pragma": "no-cache",
    "Referer": "https://p60718618653004equ-saas.yl-activity.meta-xuantan.com/activityMultiport.html?appKey=hdzy_gmkjjt_aeuyur&placeId=6071861865300&activityPlanId=44993818764&applicationId=11&li=0132541916176534842173159328666627901045&hi=xmps&channelType=1050&platformEnv=4&devVersion=DV100&idxgy=89n08qvl&eoq=0dzibt7pk983",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; JER-AN20 Build/HUAWEIJER-AN20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/142.0.7444.172 Mobile Safari/537.36 XWEB/1420045 MMWEBSDK/20251006 MMWEBID/8151 MicroMessenger/8.0.66.2980(0x28004234) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 miniProgram/wx1736dcbd36f4c055",
    "X-Requested-With": "XMLHttpRequest",
    "functionId": "0",
    "nonceStr": "69e47daadf2d78aaabd5ff9b1441ded2",
    "sec-ch-ua": "\"Chromium\";v=\"142\", \"Android WebView\";v=\"142\", \"Not_A Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "xmSign": xmSign,
    "xmTimestamp": xmTimestamp
}

# cookies = {
#     "loginTime": "hdzy_gmkjjt_aeuyur=1765283550104",
#     "userId": "hdzy_gmkjjt_aeuyur=943517868434632393",
#     "ls": "hdzy_gmkjjt_aeuyur=6728655998176528354985275481656633240978-1",
#     "appKey": "hdzy_gmkjjt_aeuyur",
#     "consumerId": "hdzy_gmkjjt_aeuyur=1593914291513282561",
#     "placeId": "hdzy_gmkjjt_aeuyur=6071861865300",
#     "openId": "hdzy_gmkjjt_aeuyur=1593914291513282561",
#     "unionId": "hdzy_gmkjjt_aeuyur="
# }

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

url = "https://p60718618653004equ-saas.yl-activity.meta-xuantan.com/xm/auth/getBaseParams"


response = requests.get(url, headers=headers, cookies=cookies, params=params)

"""
返回值
{"code":"0","desc":"成功","data":{"timestamp":1765348791,"nonceStr":"9de98dfee650435eb8dc36ae9905f611","signature":"0792fe3f5a3ae436e062498e5a5ad5dd1a4e3870","authAppId":"wxc3e844ce49c652a3","componentAppId":null,"openAuthPageUrl":"https://yl-auth.meta-xuantan.com/xm_open_auth3.html?analysisUrl=","activityUrl":"p60718618653004equ-saas.yl-activity.meta-xuantan.com/xm/activity/place/6071861865300/54-92532-rrdjbfx3cd/v1-oovtu2?vs=2&appKey=hdzy_gmkjjt_aeuyur&placeId=6071861865300&sui=8047087969542797917&platform=3&env=prod&channelType=1050&putChannel=GOODME","authSwitch":"000"}}

"""
print(response.text)
print(response)