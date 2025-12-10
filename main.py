#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
古茗咖啡新年签到计划 - 主程序
Guming Coffee New Year Check-in Plan - Main Entry
"""

import json
import sys
import os
from datetime import datetime
from checkin import GumingCheckin
from wechat_pusher import WechatPusher


def load_config(config_path='config.json'):
    """加载配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ 配置文件 {config_path} 不存在！")
        print("请复制 config.example.json 为 config.json 并填入您的信息")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件格式错误: {e}")
        sys.exit(1)


def main():
    """主函数"""
    print("=" * 60)
    print("🎉 古茗咖啡新年签到计划 🎉")
    print("=" * 60)
    print(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 加载配置
    config = load_config()
    account = config.get('account', {})
    wechat_config = config.get('wechat_push', {})
    
    if not account:
        print("❌ 未配置账户信息！")
        sys.exit(1)
    
    # 验证必需参数
    host = account.get('host')
    li = account.get('li')
    eoq = account.get('eoq')
    cookies = account.get('cookies', {})
    
    if not host:
        print("❌ 配置文件缺少 host 参数！")
        print("请检查 config.json 中的 account.host 配置")
        print("示例: p60718618653004equ-saas.yl-activity.meta-xuantan.com")
        sys.exit(1)
    
    if not li or not eoq:
        print("❌ 配置文件缺少 li 或 eoq 参数！")
        print("请检查 config.json 中的 account.li 和 account.eoq 配置")
        sys.exit(1)
    
    if not cookies:
        print("❌ 未配置 Cookie 信息！")
        sys.exit(1)
    
    # 初始化微信推送器
    wechat_pusher = None
    if wechat_config.get('enabled', True):
        try:
            wechat_pusher = WechatPusher(
                corpid=wechat_config.get('corpid'),
                corpsecret=wechat_config.get('corpsecret'),
                agentid=wechat_config.get('agentid'),
                touser=wechat_config.get('touser', '@all')
            )
            print("✅ 微信推送模块已启用")
        except Exception as e:
            print(f"⚠️  微信推送模块初始化失败: {e}")
            wechat_pusher = None
    
    print()
    
    # 执行签到
    account_name = account.get('name', '未命名')
    
    checkin = GumingCheckin(
        host=host,
        li=li,
        eoq=eoq,
        cookies=cookies,
        name=account_name
    )
    
    result = checkin.run()
    
    # 发送通知
    if wechat_pusher and result:
        send_notification(wechat_pusher, account_name, result)
    
    print("\n" + "=" * 60)
    if result.get('success'):
        print("✨ 签到完成！")
    else:
        print("⚠️  签到未成功，请查看上方日志")
    print("=" * 60)


def send_notification(pusher, account_name, result):
    """发送微信通知"""
    success = result.get('success', False)
    message = result.get('message', '未知状态')
    
    # 构建消息内容
    status = "✅ 成功" if success else "❌ 失败"
    title = f"🎉 古茗签到结果通知"
    
    content_lines = [
        f"📊 签到状态: {status}",
        f"👤 账户: {account_name}",
        f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"💬 结果: {message}"
    ]
    
    # 如果有额外信息
    if result.get('date'):
        content_lines.append(f"📅 签到日期: {result.get('date')}")
    
    content = "\n".join(content_lines)
    
    # 发送推送
    try:
        pusher.send_text_message(title, content)
        print("\n✅ 微信推送发送成功！")
    except Exception as e:
        print(f"\n⚠️  微信推送发送失败: {e}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
