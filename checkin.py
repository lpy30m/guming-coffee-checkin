#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
古茗咖啡签到核心模块
Guming Coffee Check-in Core Module
"""

import time
import hashlib
import requests
from datetime import datetime


class GumingCheckin:
    """古茗咖啡签到类"""
    
    def __init__(self, phone, password):
        """
        初始化签到客户端
        
        Args:
            phone: 手机号
            password: 密码
        """
        self.phone = phone
        self.password = password
        self.session = requests.Session()
        self.token = None
        
        # 设置请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })
    
    def _encrypt_password(self, password):
        """
        加密密码（示例使用 MD5，实际需根据古茗 API 调整）
        
        Args:
            password: 明文密码
            
        Returns:
            加密后的密码
        """
        # 注意：这里需要根据实际的古茗 API 加密方式进行调整
        # 示例使用简单的 MD5 加密
        return hashlib.md5(password.encode()).hexdigest()
    
    def login(self):
        """
        登录获取 token
        
        Returns:
            bool: 登录是否成功
        """
        print(f"📱 正在登录账户: {self.phone[:3]}****{self.phone[-4:]}")
        
        # 注意：以下是示例 API 端点，需要根据实际情况调整
        # 您需要通过抓包工具（如 Charles、Fiddler）获取真实的 API 地址和参数
        
        login_url = "https://api.guming.com/api/v1/login"  # 示例 URL
        
        payload = {
            "phone": self.phone,
            "password": self._encrypt_password(self.password),
            "deviceId": "AUTO_CHECKIN_DEVICE",
            "timestamp": int(time.time() * 1000)
        }
        
        try:
            response = self.session.post(login_url, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('code') == 0 or data.get('success'):
                self.token = data.get('data', {}).get('token')
                if self.token:
                    self.session.headers['Authorization'] = f'Bearer {self.token}'
                    print("✅ 登录成功！")
                    return True
            
            print(f"❌ 登录失败: {data.get('message', '未知错误')}")
            return False
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 登录请求失败: {e}")
            return False
    
    def do_checkin(self):
        """
        执行签到
        
        Returns:
            dict: 签到结果
        """
        print("📝 正在执行签到...")
        
        # 注意：以下是示例 API 端点，需要根据实际情况调整
        checkin_url = "https://api.guming.com/api/v1/checkin"  # 示例 URL
        
        payload = {
            "timestamp": int(time.time() * 1000),
            "source": "app"
        }
        
        try:
            response = self.session.post(checkin_url, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('code') == 0 or data.get('success'):
                reward = data.get('data', {}).get('reward', '未知奖励')
                days = data.get('data', {}).get('continueDays', 0)
                
                message = f"签到成功！获得 {reward}，已连续签到 {days} 天"
                print(f"✅ {message}")
                
                return {
                    'success': True,
                    'message': message,
                    'reward': reward,
                    'days': days
                }
            else:
                error_msg = data.get('message', '未知错误')
                print(f"❌ 签到失败: {error_msg}")
                
                return {
                    'success': False,
                    'message': error_msg
                }
                
        except requests.exceptions.RequestException as e:
            error_msg = f"签到请求失败: {e}"
            print(f"❌ {error_msg}")
            
            return {
                'success': False,
                'message': error_msg
            }
    
    def run(self):
        """
        执行完整的签到流程
        
        Returns:
            dict: 签到结果
        """
        # 登录
        if not self.login():
            return {
                'success': False,
                'message': '登录失败'
            }
        
        # 等待一下，模拟真实用户行为
        time.sleep(1)
        
        # 执行签到
        return self.do_checkin()


if __name__ == '__main__':
    # 测试代码
    print("⚠️  这是签到模块，请运行 main.py 来执行完整的签到流程")
    print("📝 注意：您需要通过抓包工具获取真实的 API 地址并修改此文件")
