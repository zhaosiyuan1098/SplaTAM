import pyrealsense2 as rs
import numpy as np
import cv2
import os
import time

# 创建子目录
os.makedirs('rgb', exist_ok=True)
os.makedirs('depth', exist_ok=True)

# 创建文件
accelerometer_file = open('accelerometer.txt', 'w')
depth_file = open('depth.txt', 'w')
groundtruth_file = open('groundtruth.txt', 'w')
rgb_file = open('rgb.txt', 'w')

# 配置深度和颜色流
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.accel, rs.format.motion_xyz32f, 250)
config.enable_stream(rs.stream.gyro, rs.format.motion_xyz32f, 200)

# 开始流
profile = pipeline.start(config)

try:
    while True:
        # 等待一组帧
        frames = pipeline.wait_for_frames()

        # 获取每一帧
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        accel_frame = frames.first_or_default(rs.stream.accel)
        gyro_frame = frames.first_or_default(rs.stream.gyro)

        # 获取时间戳
        timestamp = frames.get_timestamp()

        # 获取加速度数据
        accel = accel_frame.as_motion_frame().get_motion_data()
        accelerometer_file.write(f'{timestamp},{accel.x},{accel.y},{accel.z}\n')

        # 获取位姿数据
        gyro = gyro_frame.as_motion_frame().get_motion_data()
        groundtruth_file.write(f'{timestamp},{gyro.x},{gyro.y},{gyro.z}\n')

        # 保存深度图像
        depth_image = np.asanyarray(depth_frame.get_data())
        depth_filename = f'depth/{timestamp}.png'
        cv2.imwrite(depth_filename, depth_image)
        depth_file.write(f'{timestamp},{depth_filename}\n')

        # 保存颜色图像
        color_image = np.asanyarray(color_frame.get_data())
        color_filename = f'rgb/{timestamp}.png'
        cv2.imwrite(color_filename, color_image)
        rgb_file.write(f'{timestamp},{color_filename}\n')

        # 等待一秒
        time.sleep(1)

finally:
    # 停止流
    pipeline.stop()

    # 关闭文件
    accelerometer_file.close()
    depth_file.close()
    groundtruth_file.close()
    rgb_file.close()