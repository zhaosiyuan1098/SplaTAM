import pyrealsense2 as rs
import yaml

# 创建一个管道
pipeline = rs.pipeline()

# 创建一个配置并配置管道以从设备流式传输
config = rs.config()
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

# 开始流式传输
pipeline.start(config)

# 获取深度流的内参
profile = pipeline.get_active_profile()
depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
depth_intrinsics = depth_profile.get_intrinsics()

# 获取颜色流的内参
color_profile = rs.video_stream_profile(profile.get_stream(rs.stream.color))
color_intrinsics = color_profile.get_intrinsics()

# 停止流式传输
pipeline.stop()

# 创建一个字典来保存参数
params = {
    'dataset_name': 'realsense',
    'camera_params': {
        'image_height': depth_intrinsics.height,
        'image_width': depth_intrinsics.width,
        'fx': depth_intrinsics.fx,
        'fy': depth_intrinsics.fy,
        'cx': depth_intrinsics.ppx,
        'cy': depth_intrinsics.ppy,
        'png_depth_scale': 1000.0,  # 这是一个常数，你可能需要根据你的设备进行调整
        'crop_edge': 0  # 这是一个常数，你可能需要根据你的设备进行调整
    }
}

# 将参数写入YAML文件
with open('./configs/data/realsense.yaml', 'w') as file:
    yaml.dump(params, file, default_flow_style=False)