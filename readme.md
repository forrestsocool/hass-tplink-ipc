# TP-Link 摄像头 HACS 集成

适用于大部分中国大陆的 TP-Link 摄像头，需要设备支持手机 APP 局域网控制。

主要实现两个功能：

1. **镜头遮蔽**

2. 对话（实际是设置为 homeassistant 的播放器）【实验性质】


## 安装/更新

#### HACS直接安装

[![Install repository](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=forrestsocool&repository=hass-tplink-ipc&category=integration)

#### 手动安装

[下载](https://github.com/bingooo/hass-tplink-ipc/archive/main.zip) 解压并复制 `custom_components/hass-tplink-ipc` 文件夹到HA配置目录下的`custom_components` 文件夹内


## 配置

设置 - 设备与服务 - 集成 - 添加集成 - "TP-Link IPC"

> 默认用户名可能是 admin，以实际摄像头为准

## 使用

### 开关摄像头遮蔽

见集成设备中的开关

如果配合 WebRTC Camera 使用，可以在画面增加一个自定义按钮，点击切换遮蔽状态。示例：

```
shortcuts:
- name: 镜头遮蔽
icon: mdi:camera-flip-outline
service: switch.toggle
service_data:
entity_id: switch.tp_link_camera_192_168_1_2_lens_mask
```

### 播放音频

在集成设备中找到 "Speaker"，点击后选择播放的媒体即可。或者在 homeassistant 侧边菜单中选择 "媒体" - 右下角切换播放设备为对应摄像头即可。

推荐使用 TTS 来测试效果，安装 "[Microsoft Edge TTS for Home Assistant](https://github.com/hasscc/hass-edge-tts/tree/main)" 后选择 Edge TTS 输入中文即可播放。

