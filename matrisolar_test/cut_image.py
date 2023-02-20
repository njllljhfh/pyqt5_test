# -*- coding:utf-8 -*-
import cv2
import numpy as np

"""接线盒抠图，拼图"""

source_path = "images/module.jpg"
wire_box_path = "./images/wire_box.jpg"
result_path = "./images/wire_box_multi.jpg"

img = cv2.imread(source_path)
print(img.shape)

width = 970
height = 360
row_start = 0
row_end = row_start + height
column_start = 1700
column_end = column_start + width
cropped = img[row_start:row_end, column_start:column_end]
print(cropped.shape)
cv2.imwrite(wire_box_path, cropped)

imgs = [cropped for _ in range(9)]
result_img = np.hstack(imgs)
print(result_img.shape)

cv2.imwrite(result_path, result_img)
