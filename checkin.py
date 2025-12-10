#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
古茗咖啡签到核心模块
Guming Coffee Check-in Core Module
"""

import time
import hashlib
import base64
import requests
import secrets
import string
import json
from datetime import datetime


class GumingCheckin:
    """古茗咖啡签到类"""
    
    # 固定密钥
    SECRET_KEY = "uh3$Hg&^HK876%gbxVG7f$%p=0M~>s1x"
    TOKEN_SECRET = "J7h8&^Bgs5#bn*7hn%!=kh308*bv2!s^"
    
    def __init__(self, host, li, eoq, cookies, name="未命名"):
        """
        初始化签到客户端
        
        Args:
            host: 请求域名（如: p60718618653004equ-saas.yl-activity.meta-xuantan.com）
            li: 活动链接参数 li
            eoq: 活动链接参数 eoq
            cookies: Cookie 字典
            name: 账户备注名
        """
        self.host = host
        self.li = li
        self.eoq = eoq
        self.cookies = cookies
        self.name = name
        self.session = requests.Session()
        self.xm_token = None
        
        # 构建页面URL
        self.page_url = (
            f"https://{host}/"
            f"activityMultiport.html?"
            f"appKey=hdzy_gmkjjt_aeuyur&placeId=6071861865300&"
            f"activityPlanId=44993818764&applicationId=11&"
            f"li={li}&hi=xmps&channelType=1050&platformEnv=4&"
            f"devVersion=DV100&idxgy=89n08qvl&eoq={eoq}"
        )
        
        # 设置基础请求头
        self.base_headers = {
            "Accept": "application/json",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Pragma": "no-cache",
            "Referer": self.page_url,
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android 12; JER-AN20 Build/HUAWEIJER-AN20; wv) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
                "Chrome/142.0.7444.172 Mobile Safari/537.36 XWEB/1420045 "
                "MMWEBSDK/20251006 MMWEBID/8151 MicroMessenger/8.0.66.2980(0x28004234) "
                "WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 "
                "miniProgram/wx1736dcbd36f4c055"
            ),
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Chromium";v="142", "Android WebView";v="142", "Not_A Brand";v="99"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
        }
        
        # 设置 Cookies
        self._setup_cookies()
    
    def _setup_cookies(self):
        """设置 Cookie 到 session"""
        for key, value in self.cookies.items():
            self.session.cookies.set(key, value)
    
    @staticmethod
    def generate_nonce_str(length=32):
        """
        生成随机字符串
        精确模拟 JS 代码的 nonceStr 生成逻辑
        """
        random_bytes = secrets.token_bytes(length)
        result = ""
        
        for byte in random_bytes:
            t = byte & 63  # 取低6位
            
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
    
    def build_get_sign(self, params):
        """
        生成 GET 请求的 xmSign
        
        Args:
            params: 请求参数字典
            
        Returns:
            xmSign 字符串
        """
        # 按 key 排序
        sorted_keys = sorted(params.keys())
        
        # 拼接参数值
        concat_str = ""
        for key in sorted_keys:
            value = params[key]
            if isinstance(value, dict):
                concat_str += json.dumps(value, separators=(',', ':'))
            else:
                concat_str += str(value)
        
        # 加密钥后计算 MD5
        sign_str = concat_str + self.SECRET_KEY
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    
    def build_token_sign(self, nonce_str, timestamp):
        """
        生成 tokenSign
        
        Args:
            nonce_str: 随机字符串
            timestamp: 时间戳
            
        Returns:
            tokenSign 字符串
        """
        sign_str = self.li + nonce_str + timestamp + self.TOKEN_SECRET
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    
    def build_post_sign(self, data, nonce_str, timestamp, xm_token=""):
        """
        生成 POST 请求的 xmSign
        
        Args:
            data: 请求 body 数据（字典）
            nonce_str: 随机字符串
            timestamp: 时间戳（字符串或整数）
            xm_token: token（可选）
            
        Returns:
            xmSign 字符串
        """
        # 合并所有参数
        sign_params = {
            **data,
            "nonceStr": nonce_str,
            "xmTimestamp": str(timestamp),
            "xmToken": xm_token,
        }
        
        # 按 key 排序
        sorted_keys = sorted(sign_params.keys())
        
        # 拼接参数值
        concat_str = ""
        for key in sorted_keys:
            value = sign_params[key]
            if isinstance(value, (dict, list)):
                concat_str += json.dumps(value, separators=(',', ':'), ensure_ascii=False)
            else:
                concat_str += str(value)
        
        # 加密钥后计算 MD5
        sign_str = concat_str + self.SECRET_KEY
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    
    def step1_get_base_params(self):
        """
        步骤1: 获取基础参数
        发送请求但不需要处理返回值
        
        Returns:
            bool: 是否成功
        """
        print(f"📝 步骤1: 获取基础参数...")
        
        url = f"https://{self.host}/xm/auth/getBaseParams"
        
        xm_timestamp = str(int(time.time() * 1000))
        nonce_str = self.generate_nonce_str()
        
        params = {
            "pageUrl": self.page_url,
            "nonceStr": nonce_str,
            "xmTimestamp": xm_timestamp
        }
        
        xm_sign = self.build_get_sign(params)
        
        headers = {
            **self.base_headers,
            "functionId": "0",
            "nonceStr": nonce_str,
            "xmSign": xm_sign,
            "xmTimestamp": xm_timestamp,
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }
        
        try:
            response = self.session.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('code') == '0' and data.get('desc') == '成功':
                print(f"✅ 步骤1完成: 基础参数请求成功")
                return True
            else:
                print(f"⚠️  步骤1: {data.get('desc', '未知错误')}")
                return False
                
        except Exception as e:
            print(f"❌ 步骤1失败: {e}")
            return False
    
    def step2_get_user_token(self):
        """
        步骤2: 获取用户 Token
        
        Returns:
            str: xmToken，失败返回 None
        """
        print(f"📝 步骤2: 获取用户 Token...")
        
        url = f"https://{self.host}/xm/token/getUserToken"
        
        xm_timestamp = str(int(time.time() * 1000))
        nonce_str_header = self.generate_nonce_str()
        nonce_str_param = self.generate_nonce_str()
        
        # URL 参数
        params = {
            "timestamp": xm_timestamp,
            "nonceStr": nonce_str_param,
            "tokenSign": self.build_token_sign(nonce_str_param, xm_timestamp)
        }
        
        # 用于签名的参数（使用 header 中的 nonceStr）
        sign_params = {
            **params,
            "nonceStr": nonce_str_header,
            "xmTimestamp": xm_timestamp,
        }
        
        xm_sign = self.build_get_sign(sign_params)
        
        headers = {
            **self.base_headers,
            "Host": self.host,
            "xmSign": xm_sign,
            "xmTimestamp": xm_timestamp,
            "xmToken": "",
            "bdrk": "null",
            "nonceStr": nonce_str_header,
            "ri": "",
            "functionId": "0",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
        }
        
        try:
            response = self.session.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('code') == '0' and data.get('desc') == '成功':
                xm_token = data.get('data')
                if xm_token:
                    self.xm_token = xm_token
                    print(f"✅ 步骤2完成: 获取 Token 成功")
                    return xm_token
                else:
                    print(f"❌ 步骤2失败: 未返回 Token")
                    return None
            else:
                print(f"❌ 步骤2失败: {data.get('desc', '未知错误')}")
                return None
                
        except Exception as e:
            print(f"❌ 步骤2失败: {e}")
            return None
    
    def step3_sign_action(self):
        """
        步骤3: 执行签到
        
        Returns:
            dict: 签到结果
        """
        print(f"📝 步骤3: 执行签到...")
        
        if not self.xm_token:
            return {
                'success': False,
                'message': '缺少 xmToken，无法签到'
            }
        
        url = f"https://{self.host}/sign/action"
        
        # 获取当前日期
        today = datetime.now().strftime('%Y-%m-%d')
        
        xm_timestamp = str(int(time.time() * 1000))
        nonce_str = self.generate_nonce_str()
        
        # POST 请求体
        post_data = {
            "patchDate": today
        }
        
        # 生成签名
        xm_sign = self.build_post_sign(post_data, nonce_str, xm_timestamp, self.xm_token)
        
        headers = {
            **self.base_headers,
            "sec-ch-ua-platform": '"Android"',
            "xmSign": xm_sign,
            "sec-ch-ua": '"Chromium";v="142", "Android WebView";v="142", "Not_A Brand";v="99"',
            "sec-ch-ua-mobile": "?1",
            "bdrk": "null",
            "xmToken": self.xm_token,
            "nonceStr": nonce_str,
            "xmTimestamp": xm_timestamp,
            "ri": "",
            "functionId": "0",
        }
        
        try:
            response = self.session.post(url, headers=headers, json=post_data, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            desc = data.get('desc', '')
            
            if desc == '成功':
                message = f"签到成功！日期: {today}"
                print(f"✅ {message}")
                
                return {
                    'success': True,
                    'message': message,
                    'date': today,
                    'response': data
                }
            elif '重复签到' in desc or '已签到' in desc or '已经签到' in desc:
                message = f"今日已签到"
                print(f"ℹ️  {message}")
                
                return {
                    'success': True,
                    'message': message,
                    'already_signed': True
                }
            else:
                print(f"❌ 签到失败: {desc}")
                
                return {
                    'success': False,
                    'message': desc
                }
                
        except Exception as e:
            error_msg = f"签到请求失败: {e}"
            print(f"❌ {error_msg}")
            
            return {
                'success': False,
                'message': error_msg
            }
    
    def do_checkin(self):
        """
        执行完整的签到流程
        
        Returns:
            dict: 签到结果
        """
        print(f"🎯 开始签到: {self.name}")
        print("=" * 50)
        
        # 步骤1: 获取基础参数
        if not self.step1_get_base_params():
            return {
                'success': False,
                'message': '步骤1: 获取基础参数失败'
            }
        
        # 等待一下，模拟真实用户
        time.sleep(0.5)
        
        # 步骤2: 获取用户 Token
        if not self.step2_get_user_token():
            return {
                'success': False,
                'message': '步骤2: 获取用户 Token 失败'
            }
        
        # 等待一下
        time.sleep(0.5)
        
        # 步骤3: 执行签到
        result = self.step3_sign_action()
        
        print("=" * 50)
        return result
    
    def run(self):
        """
        执行签到流程的入口方法
        
        Returns:
            dict: 签到结果
        """
        return self.do_checkin()


if __name__ == '__main__':
    print("⚠️  这是签到模块，请运行 main.py 来执行完整的签到流程")
    print("📝 使用 li、eoq 和 Cookie 认证方式")
