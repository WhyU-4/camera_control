#!/usr/bin/env python3
"""
ONVIF PTZ Camera Control
This script provides control for PTZ (Pan-Tilt-Zoom) cameras using the ONVIF protocol.
"""

from onvif import ONVIFCamera
import sys
import time
import os


class PTZCameraControl:
    """控制ONVIF云台相机的类"""
    
    def __init__(self, ip, port, username, password):
        """
        初始化相机连接
        
        Args:
            ip: 相机IP地址
            port: ONVIF端口 (默认81)
            username: 登录用户名
            password: 登录密码
        """
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.camera = None
        self.ptz = None
        self.media_profile = None
        
    def connect(self):
        """连接到相机"""
        try:
            print(f"正在连接到相机 {self.ip}:{self.port}...")
            self.camera = ONVIFCamera(self.ip, self.port, self.username, self.password)
            
            # 获取媒体服务
            media_service = self.camera.create_media_service()
            
            # 获取媒体配置文件
            profiles = media_service.GetProfiles()
            if not profiles:
                raise Exception("没有找到媒体配置文件")
            
            self.media_profile = profiles[0]
            print(f"使用媒体配置文件: {self.media_profile.Name}")
            
            # 创建PTZ服务
            self.ptz = self.camera.create_ptz_service()
            print("成功连接到相机!")
            return True
            
        except Exception as e:
            print(f"连接失败: {e}")
            return False
    
    def get_ptz_configuration(self):
        """获取PTZ配置"""
        try:
            request = self.ptz.create_type('GetConfigurationOptions')
            request.ConfigurationToken = self.media_profile.PTZConfiguration.token
            ptz_config = self.ptz.GetConfigurationOptions(request)
            return ptz_config
        except Exception as e:
            print(f"获取PTZ配置失败: {e}")
            return None
    
    def move_continuous(self, pan_velocity, tilt_velocity, zoom_velocity=0, timeout=1, wait=False):
        """
        持续移动相机
        
        Args:
            pan_velocity: 水平移动速度 (-1.0 到 1.0)
            tilt_velocity: 垂直移动速度 (-1.0 到 1.0)
            zoom_velocity: 缩放速度 (-1.0 到 1.0)
            timeout: 移动持续时间（秒）
            wait: 是否等待移动完成
        """
        try:
            request = self.ptz.create_type('ContinuousMove')
            request.ProfileToken = self.media_profile.token
            
            # 设置速度
            request.Velocity = {
                'PanTilt': {'x': pan_velocity, 'y': tilt_velocity},
                'Zoom': {'x': zoom_velocity}
            }
            
            # 设置超时
            if timeout:
                request.Timeout = f"PT{timeout}S"
            
            self.ptz.ContinuousMove(request)
            print(f"移动: Pan={pan_velocity}, Tilt={tilt_velocity}, Zoom={zoom_velocity}")
            
            # ContinuousMove是异步的，需要等待完成
            if wait:
                time.sleep(timeout)
            
        except Exception as e:
            print(f"移动失败: {e}")
    
    def stop(self):
        """停止所有移动"""
        try:
            request = self.ptz.create_type('Stop')
            request.ProfileToken = self.media_profile.token
            request.PanTilt = True
            request.Zoom = True
            self.ptz.Stop(request)
            print("已停止移动")
        except Exception as e:
            print(f"停止失败: {e}")
    
    def move_left(self, speed=0.5, duration=1):
        """向左移动"""
        print("向左移动...")
        self.move_continuous(-speed, 0, 0, duration, wait=True)
        self.stop()
    
    def move_right(self, speed=0.5, duration=1):
        """向右移动"""
        print("向右移动...")
        self.move_continuous(speed, 0, 0, duration, wait=True)
        self.stop()
    
    def move_up(self, speed=0.5, duration=1):
        """向上移动"""
        print("向上移动...")
        self.move_continuous(0, speed, 0, duration, wait=True)
        self.stop()
    
    def move_down(self, speed=0.5, duration=1):
        """向下移动"""
        print("向下移动...")
        self.move_continuous(0, -speed, 0, duration, wait=True)
        self.stop()
    
    def zoom_in(self, speed=0.5, duration=1):
        """放大"""
        print("放大...")
        self.move_continuous(0, 0, speed, duration, wait=True)
        self.stop()
    
    def zoom_out(self, speed=0.5, duration=1):
        """缩小"""
        print("缩小...")
        self.move_continuous(0, 0, -speed, duration, wait=True)
        self.stop()
    
    def goto_home_position(self):
        """回到预设的起始位置"""
        try:
            request = self.ptz.create_type('GotoHomePosition')
            request.ProfileToken = self.media_profile.token
            self.ptz.GotoHomePosition(request)
            print("返回起始位置")
        except Exception as e:
            print(f"返回起始位置失败: {e}")
    
    def set_home_position(self):
        """设置当前位置为起始位置"""
        try:
            request = self.ptz.create_type('SetHomePosition')
            request.ProfileToken = self.media_profile.token
            self.ptz.SetHomePosition(request)
            print("已设置当前位置为起始位置")
        except Exception as e:
            print(f"设置起始位置失败: {e}")
    
    def get_status(self):
        """获取PTZ状态"""
        try:
            request = self.ptz.create_type('GetStatus')
            request.ProfileToken = self.media_profile.token
            status = self.ptz.GetStatus(request)
            print(f"当前位置: Pan={status.Position.PanTilt.x}, Tilt={status.Position.PanTilt.y}, Zoom={status.Position.Zoom.x}")
            return status
        except Exception as e:
            print(f"获取状态失败: {e}")
            return None


def main():
    """主函数 - 演示PTZ控制功能"""
    
    # 相机配置 - 支持环境变量覆盖，默认使用指定的配置
    CAMERA_IP = os.getenv("CAMERA_IP", "192.168.1.21")
    CAMERA_PORT = int(os.getenv("CAMERA_PORT", "81"))
    USERNAME = os.getenv("CAMERA_USERNAME", "admin")
    PASSWORD = os.getenv("CAMERA_PASSWORD", "888888")
    
    # 创建相机控制对象
    ptz_camera = PTZCameraControl(CAMERA_IP, CAMERA_PORT, USERNAME, PASSWORD)
    
    # 连接到相机
    if not ptz_camera.connect():
        print("无法连接到相机，退出程序")
        sys.exit(1)
    
    # 显示菜单
    while True:
        print("\n" + "="*50)
        print("PTZ 相机控制菜单")
        print("="*50)
        print("1. 向左移动")
        print("2. 向右移动")
        print("3. 向上移动")
        print("4. 向下移动")
        print("5. 放大 (Zoom In)")
        print("6. 缩小 (Zoom Out)")
        print("7. 获取当前状态")
        print("8. 回到起始位置")
        print("9. 设置当前位置为起始位置")
        print("0. 退出")
        print("="*50)
        
        choice = input("请选择操作 (0-9): ").strip()
        
        if choice == '1':
            ptz_camera.move_left()
        elif choice == '2':
            ptz_camera.move_right()
        elif choice == '3':
            ptz_camera.move_up()
        elif choice == '4':
            ptz_camera.move_down()
        elif choice == '5':
            ptz_camera.zoom_in()
        elif choice == '6':
            ptz_camera.zoom_out()
        elif choice == '7':
            ptz_camera.get_status()
        elif choice == '8':
            ptz_camera.goto_home_position()
        elif choice == '9':
            ptz_camera.set_home_position()
        elif choice == '0':
            print("退出程序")
            break
        else:
            print("无效的选择，请重试")
        
        time.sleep(0.5)


if __name__ == "__main__":
    main()
