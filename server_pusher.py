#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Server 酱推送模块
Server Chan Push Module
"""

import requests


class ServerPusher:
    """Server 酱推送类"""
    
    def __init__(self, sendkey):
        """
        初始化 Server 酱推送器
        
        Args:
            sendkey: Server 酱的 SendKey
        """
        self.sendkey = sendkey
        self.api_url = f'https://sctapi.ftqq.com/{self.sendkey}.send'
    
    def send(self, title, desp='', options=None):
        """
        发送推送消息
        
        Args:
            title: 消息标题
            desp: 消息内容
            options: 其他选项（可选）
            
        Returns:
            dict: API 返回结果
        """
        if options is None:
            options = {}
        
        params = {
            'title': title,
            'desp': desp,
            **options
        }
        
        headers = {
            'Content-Type': 'application/json;charset=utf-8'
        }
        
        try:
            response = requests.post(self.api_url, json=params, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if result.get('code') == 0:
                return result
            else:
                raise Exception(f"Server 酱推送失败: {result.get('message', '未知错误')}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Server 酱请求失败: {e}")


if __name__ == '__main__':
    # 测试代码
    print("⚠️  这是推送模块，请在 config.json 中配置 sendkey")
    print("📝 获取 SendKey: https://sct.ftqq.com/")