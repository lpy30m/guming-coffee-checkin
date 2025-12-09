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
    print("=" * 50)
    print("🎉 古茗咖啡新年签到计划 🎉")
    print("=" * 50)
    print(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 加载配置
    config = load_config()
    accounts = config.get('accounts', [])
    wechat_config = config.get('wechat_push', {})
    
    if not accounts:
        print("❌ 未配置任何账户！")
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
    
    # 执行签到
    results = []
    for idx, account in enumerate(accounts, 1):
        print(f"\n--- 账户 {idx}/{len(accounts)}: {account.get('name', '未命名')} ---")
        
        checkin = GumingCheckin(
            phone=account.get('phone'),
            password=account.get('password')
        )
        
        result = checkin.run()
        results.append({
            'account': account.get('name', account.get('phone')),
            'result': result
        })
    
    # 发送汇总通知
    if wechat_pusher:
        send_summary_notification(wechat_pusher, results)
    
    print("\n" + "=" * 50)
    print("✨ 所有任务执行完成！")
    print("=" * 50)


def send_summary_notification(pusher, results):
    """发送汇总通知"""
    success_count = sum(1 for r in results if r['result']['success'])
    total_count = len(results)
    
    # 构建消息内容
    title = "🎉 古茗签到结果通知"
    
    content_lines = [
        f"📊 签到统计: {success_count}/{total_count} 成功",
        f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "详细结果:"
    ]
    
    for item in results:
        status = "✅" if item['result']['success'] else "❌"
        account = item['account']
        message = item['result']['message']
        content_lines.append(f"{status} {account}: {message}")
    
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
