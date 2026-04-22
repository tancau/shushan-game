#!/usr/bin/env python3
"""
蜀山剑侠传 - 游戏入口
"""

import os
import sys

if __name__ == '__main__':
    print("欢迎来到蜀山剑侠传！")
    print("请选择运行模式：")
    print("1. 启动后端API服务")
    print("2. 启动前端开发服务器")
    print("3. 退出")
    
    choice = input("请输入选项编号：")
    
    if choice == "1":
        print("启动后端API服务...")
        os.system("python api.py")
    elif choice == "2":
        print("启动前端开发服务器...")
        os.chdir("frontend")
        os.system("npm run dev")
    elif choice == "3":
        print("再见！")
        sys.exit(0)
    else:
        print("无效选项，请重新运行。")
        sys.exit(1)
