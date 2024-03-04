import time
import os
import cv2
import numpy as np
import pyrealsense2 as rs

# 创建一个管道
pipeline = rs.pipeline()

# 创建一个配置并配置管道以从 RealSense 设备流式传输
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)

# 开始流式传输
pipeline.start(config)

try:
    count = 0
    while True:
        # 等待一组对齐的帧
        frames = pipeline.wait_for_frames()

        # 获取对齐的帧
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        # 验证两个帧是否有效
        if not depth_frame or not color_frame:
            continue

        # 将帧转换为 numpy 数组
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # 创建目录
        rgb_dir = './data/realsense/test0sleep/rgb'
        depth_dir = './data/realsense/test0sleep/depth'
        os.makedirs(rgb_dir, exist_ok=True)
        os.makedirs(depth_dir, exist_ok=True)

        # 保存图像
        cv2.imwrite(os.path.join(rgb_dir, f'{count}.png'), color_image)
        cv2.imwrite(os.path.join(depth_dir, f'{count}.png'), depth_image)
        print(count)
        # 每隔一秒保存一次
        time.sleep(0.0001)
        count += 1

finally:
    # 停止流式传输
    pipeline.stop()
