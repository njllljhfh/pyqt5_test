# -*- coding:utf-8 -*-
import numpy as np
import cv2

# 创建一个1000x800的黑色图像
width, height = 1000, 800
black_image = np.zeros((height, width, 3), dtype=np.uint8)  # 使用uint8表示像素值范围为0-255

# 将图像保存为二进制数据
_, img_np = cv2.imencode('.jpg', black_image)

# print(type(binary_data))
print(type(black_image))
binary_data = img_np.tobytes()
print(type(binary_data))

# 将二进制数据保存到文件或进行其他处理
with open('black_image.jpg', 'wb') as file:
    file.write(binary_data)
