#!/usr/bin/env python3
"""
示例脚本：演示如何使用PTZCameraControl类
Example script: Demonstrates how to use the PTZCameraControl class
"""

from camera_control import PTZCameraControl
import time
import os


def example_usage():
    """演示基本的相机控制功能"""
    
    # 相机配置 - 支持环境变量覆盖，默认使用指定的配置
    CAMERA_IP = os.getenv("CAMERA_IP", "192.168.1.21")
    CAMERA_PORT = int(os.getenv("CAMERA_PORT", "81"))
    USERNAME = os.getenv("CAMERA_USERNAME", "admin")
    PASSWORD = os.getenv("CAMERA_PASSWORD", "888888")
    
    # 创建相机控制对象
    camera = PTZCameraControl(CAMERA_IP, CAMERA_PORT, USERNAME, PASSWORD)
    
    # 连接到相机
    if not camera.connect():
        print("无法连接到相机")
        return
    
    print("\n开始演示相机控制功能...")
    
    # 1. 获取当前状态
    print("\n1. 获取当前状态")
    camera.get_status()
    time.sleep(2)
    
    # 2. 向右移动
    print("\n2. 向右移动")
    camera.move_right(speed=0.3, duration=2)
    time.sleep(1)
    
    # 3. 向左移动
    print("\n3. 向左移动")
    camera.move_left(speed=0.3, duration=2)
    time.sleep(1)
    
    # 4. 向上移动
    print("\n4. 向上移动")
    camera.move_up(speed=0.3, duration=2)
    time.sleep(1)
    
    # 5. 向下移动
    print("\n5. 向下移动")
    camera.move_down(speed=0.3, duration=2)
    time.sleep(1)
    
    # 6. 放大
    print("\n6. 放大")
    camera.zoom_in(speed=0.3, duration=2)
    time.sleep(1)
    
    # 7. 缩小
    print("\n7. 缩小")
    camera.zoom_out(speed=0.3, duration=2)
    time.sleep(1)
    
    # 8. 获取最终状态
    print("\n8. 获取最终状态")
    camera.get_status()
    
    print("\n演示完成！")


if __name__ == "__main__":
    example_usage()
