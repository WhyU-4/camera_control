# camera_control

基于ONVIF协议的Python云台相机(PTZ)控制系统

## 功能特性

- 支持ONVIF协议的云台相机控制
- 提供完整的PTZ（Pan-Tilt-Zoom）控制功能
- 支持连续移动和精确控制
- 交互式菜单界面
- 预设位置管理

## 系统要求

- Python 3.6+
- 支持ONVIF协议的PTZ相机

## 安装

1. 克隆仓库:
```bash
git clone https://github.com/WhyU-4/camera_control.git
cd camera_control
```

2. 安装依赖:
```bash
pip install -r requirements.txt
```

## 配置

默认相机配置:
- IP地址: 192.168.1.21
- 端口: 80
- 用户名: admin
- 密码: 888888

如需修改配置，请编辑 `camera_control.py` 或 `example.py` 中的相机参数。

## 使用方法

### 方法1: 交互式菜单

运行主程序，使用交互式菜单控制相机:

```bash
python camera_control.py
```

菜单选项:
1. 向左移动
2. 向右移动
3. 向上移动
4. 向下移动
5. 放大 (Zoom In)
6. 缩小 (Zoom Out)
7. 获取当前状态
8. 回到起始位置
9. 设置当前位置为起始位置
0. 退出

### 方法2: 编程方式

运行示例脚本:

```bash
python example.py
```

或在你的代码中使用:

```python
from camera_control import PTZCameraControl

# 创建相机控制对象
camera = PTZCameraControl("192.168.1.21", 80, "admin", "888888")

# 连接到相机
if camera.connect():
    # 控制相机
    camera.move_right(speed=0.5, duration=2)
    camera.zoom_in(speed=0.3, duration=1)
    camera.get_status()
```

## API 说明

### PTZCameraControl 类

#### 初始化
```python
camera = PTZCameraControl(ip, port, username, password)
```

#### 主要方法

- `connect()` - 连接到相机
- `move_left(speed, duration)` - 向左移动
- `move_right(speed, duration)` - 向右移动
- `move_up(speed, duration)` - 向上移动
- `move_down(speed, duration)` - 向下移动
- `zoom_in(speed, duration)` - 放大
- `zoom_out(speed, duration)` - 缩小
- `stop()` - 停止所有移动
- `get_status()` - 获取当前PTZ状态
- `goto_home_position()` - 回到起始位置
- `set_home_position()` - 设置当前位置为起始位置
- `move_continuous(pan, tilt, zoom, timeout)` - 自定义连续移动

#### 参数说明

- `speed`: 移动速度，范围 0.0 到 1.0
- `duration`: 移动持续时间（秒）
- `pan`: 水平移动速度，范围 -1.0 到 1.0
- `tilt`: 垂直移动速度，范围 -1.0 到 1.0
- `zoom`: 缩放速度，范围 -1.0 到 1.0

## 注意事项

1. 确保相机和运行此脚本的设备在同一网络中
2. 确认相机已启用ONVIF服务
3. 相机的IP地址、用户名和密码必须正确
4. 部分相机可能需要在设置中启用ONVIF协议支持

## 故障排除

### 连接失败
- 检查相机IP地址是否正确
- 确认相机和电脑在同一网络
- 验证用户名和密码
- 确认相机已启用ONVIF服务

### 功能不响应
- 确认相机支持PTZ功能
- 检查相机PTZ配置是否正确
- 尝试重启相机

## 许可证

MIT License

## 贡献

欢迎提交问题和拉取请求!
