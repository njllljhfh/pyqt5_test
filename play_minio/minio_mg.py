# -*- coding:utf-8 -*-
import os
from io import BytesIO

from minio import Minio
from minio.error import *

# MinIo配置参数
MINIO_ENDPOINT = "10.0.1.110:9000"
MINIO_ACCESS_KEY = "adc5000"
MINIO_SECRET_KEY = "adc5000adc"
# MINIO_SECURE = False
# MINIO_BUCKET = "adc5000"
# MINIO_INFER_RESULT_BUCKET = "inferresult"
MINIO_SECURE = False
MINIO_BUCKET = "dragon"

if __name__ == '__main__':
    minioClient = Minio(MINIO_ENDPOINT,
                        access_key=MINIO_ACCESS_KEY,
                        secret_key=MINIO_SECRET_KEY,
                        secure=MINIO_SECURE)

    # 调用make_bucket来创建一个存储桶。
    try:
        if not minioClient.bucket_exists(MINIO_BUCKET):
            minioClient.make_bucket(MINIO_BUCKET, location="us-east-1")
        else:
            print(f'bucket"{MINIO_BUCKET}"已存在，无需创建')
    except MinioException as e:
        print(f'错误:{e}')

    local_files_path = './local_data_path/files'

    # 上传本地文件到minio
    minio_files_path = '/files/f1.txt'
    try:
        res = minioClient.fput_object(MINIO_BUCKET,
                                      minio_files_path,
                                      f'{local_files_path}/f1.txt')
        print(f'res = {res}')
    except MinioException as err:
        print(f'错误:{e}')

    local_images_path = './local_data_path/images'
    # 上传流到minio
    try:
        image_path = f'{local_images_path}/img1.jpg'
        with open(image_path, 'rb') as f:
            content = f.read()
            img_buffer = BytesIO(content)
            size = len(content)
            minio_image_path = '/images/img1.jpg'
            res = minioClient.put_object(MINIO_BUCKET, minio_image_path, img_buffer, size)
        # print(f'res = {res}')
    except MinioException as err:
        print(f'错误:{e}')

    # 从minio读取图像文件
    download_path = './download'
    try:
        data = minioClient.get_object(MINIO_BUCKET, minio_image_path)
        img_download_path = f'{download_path}/1.jpg'
        with open(img_download_path, 'wb') as file_data:
            # file_data.write(data.data)
            for d in data.stream(1024):
                file_data.write(d)
    except MinioException as err:
        print(f'错误:{e}')

    # 从minio读取文本文件
    try:
        data = minioClient.get_object(MINIO_BUCKET, minio_files_path)
        download_path = './download'
        img_download_path = f'{download_path}/1.txt'
        with open(img_download_path, 'wb') as file_data:
            # file_data.write(data.data)
            for d in data.stream(1024):
                file_data.write(d)
    except MinioException as err:
        print(f'错误:{e}')
