# -*- coding:utf-8 -*-
import os

import cv2


class Compress_img:

    def __init__(self, img_root_dir):
        # self.img_path = img_path
        # self.img_name = img_path.split('/')[-1]

        self.img_root_dir = img_root_dir

    def compress_img_CV(self, compress_rate=0.5, show=False):

        for root, dirs, files in os.walk(self.img_root_dir):
            # print(root)
            # print(dirs)
            # print(files)
            for img_name in files:
                # print(f'{img_name}')
                img_path = os.path.join(root, img_name)
                # print(f'{img_path}')
                img_name: str
                new_dir = 'D:\\quadrate-wafer\\Test-compress'
                if img_name.endswith(('.png', '.jpeg', 'jpg')):
                    print(f'{img_path}')
                    new_img_path = os.path.join(new_dir, img_name)
                    # print(f'{new_img_path}')

                    img = cv2.imread(img_path)
                    heigh, width = img.shape[:2]
                    # 双三次插值
                    img_resize = cv2.resize(img, (int(heigh * compress_rate), int(width * compress_rate)),
                                            interpolation=cv2.INTER_AREA)
                    cv2.imwrite(new_img_path, img_resize)

                    print("%s 已压缩，" % (img_name), "压缩率：", compress_rate)

                    # if show:
                    #     cv2.imshow(self.img_name, img_resize)
                    #     cv2.waitKey(0)


if __name__ == '__main__':
    img_path = 'D:\\quadrate-wafer\\Test-source'
    compress = Compress_img(img_path)

    # 使用opencv压缩图片
    compress.compress_img_CV()
