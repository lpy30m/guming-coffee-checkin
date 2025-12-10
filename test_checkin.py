#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 用于验证签到流程
"""

import json
from checkin import GumingCheckin

def test_checkin():
    """测试签到流程"""
    print("=" * 60)
    print("🧪 古茗签到流程测试")
    print("=" * 60)
    print()
    
    # 从 config.json 读取配置
    try:
        with open('古茗/签到活动/config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ config.json 不存在")
        print("请先创建配置文件：cp config.example.json config.json")
        return
    
    account = config.get('account', {})
    
    # 验证配置
    host = account.get('host')
    li = account.get('li')
    url_params = account.get('url_params', {})
    cookies = account.get('cookies', {})
    name = account.get('name', '测试账号')
    
    if not host:
        print("❌ 配置文件缺少 host 参数")
        return
    
    if not li:
        print("❌ 配置文件缺少 li 参数")
        return
    
    if not url_params:
        print("❌ 配置文件缺少 url_params 参数")
        return
    
    if not cookies:
        print("❌ 配置文件缺少 cookies")
        return
    
    print(f"📋 配置检查:")
    print(f"  - 账户名称: {name}")
    print(f"  - Host: {host}")
    print(f"  - li 参数: {li[:20]}...")
    print(f"  - URL 参数: {url_params}")
    print(f"  - Cookie 字段数: {len(cookies)}")
    print()
    
    # 创建签到实例
    checkin = GumingCheckin(
        host=host,
        li=li,
        url_params=url_params,
        cookies=cookies,
        name=name
    )
    
    # 执行签到
    result = checkin.run()
    
    # 输出结果
    print()
    print("=" * 60)
    print("📊 测试结果:")
    print("=" * 60)
    print(f"状态: {'✅ 成功' if result.get('success') else '❌ 失败'}")
    print(f"消息: {result.get('message')}")
    
    if result.get('date'):
        print(f"日期: {result.get('date')}")
    
    if result.get('already_signed'):
        print("(今日已签到过)")
    
    print("=" * 60)
    
    return result.get('success')


if __name__ == '__main__':
    success = test_checkin()
    exit(0 if success else 1)
