#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业微信推送模块
WeChat Work Push Module
"""

import requests
import time


class WechatPusher:
    """企业微信推送类"""
    
    def __init__(self, corpid, corpsecret, agentid, touser='@all'):
        """
        初始化企业微信推送器
        
        Args:
            corpid: 企业微信 CorpID
            corpsecret: 应用的 CorpSecret
            agentid: 应用的 AgentID
            touser: 接收消息的用户，默认 @all 表示全部
        """
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.touser = touser
        self.access_token = None
        self.token_expires_at = 0
        
    def get_access_token(self):
        """
        获取企业微信 access_token
        
        Returns:
            str: access_token
        """
        # 如果 token 还在有效期内，直接返回
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
        
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            'corpid': self.corpid,
            'corpsecret': self.corpsecret
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('errcode') == 0:
                self.access_token = data.get('access_token')
                # 提前 5 分钟过期，避免边界情况
                expires_in = data.get('expires_in', 7200) - 300
                self.token_expires_at = time.time() + expires_in
                return self.access_token
            else:
                raise Exception(f"获取 access_token 失败: {data.get('errmsg')}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求 access_token 失败: {e}")
    
    def send_text_message(self, title, content):
        """
        发送文本消息
        
        Args:
            title: 消息标题
            content: 消息内容
            
        Returns:
            bool: 发送是否成功
        """
        access_token = self.get_access_token()
        
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
        
        # 构建消息内容
        message = f"{title}\n\n{content}"
        
        payload = {
            "touser": self.touser,
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": message
            },
            "safe": 0
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('errcode') == 0:
                return True
            else:
                raise Exception(f"发送消息失败: {data.get('errmsg')}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"发送消息请求失败: {e}")
    
    def send_markdown_message(self, content):
        """
        发送 Markdown 格式消息
        
        Args:
            content: Markdown 格式的消息内容
            
        Returns:
            bool: 发送是否成功
        """
        access_token = self.get_access_token()
        
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
        
        payload = {
            "touser": self.touser,
            "msgtype": "markdown",
            "agentid": self.agentid,
            "markdown": {
                "content": content
            },
            "safe": 0
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('errcode') == 0:
                return True
            else:
                raise Exception(f"发送消息失败: {data.get('errmsg')}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"发送消息请求失败: {e}")


if __name__ == '__main__':
    # 测试代码
    print("⚠️  这是微信推送模块，请运行 main.py 来执行完整的签到流程")
    print("📝 您需要在 config.json 中配置企业微信相关信息")
