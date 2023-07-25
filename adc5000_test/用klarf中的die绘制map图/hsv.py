# -*- coding:utf-8 -*-
import cv2


def adjust_brightness(image, brightness):
    # 将图像转换为HSV色彩空间
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 将亮度分量增加或减少指定的值
    hsv_image[:, :, 2] += brightness

    # 将调整后的图像转换回BGR色彩空间
    adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    return adjusted_image


# 加载图像
image = cv2.imread("waferMap.jpg")

# 调整亮度（增加亮度）
adjusted_image = adjust_brightness(image, 150)

# 显示调整后的图像
cv2.imshow("Adjusted Image", adjusted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
