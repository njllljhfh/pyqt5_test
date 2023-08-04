# -*- coding:utf-8 -*-
import os

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

"""
模拟web表单，上传本地目录中的全部文件
"""


def upload_files_to_server(url, local_directory):
    base_name = os.path.basename(local_image_directory)
    print(f"base_name = {base_name}")

    files_to_upload = []
    for root, dirs, files in os.walk(local_directory):
        # print(f"root = {root}")
        # print(f"dirs = {dirs}")
        # print(f"files = {files}")
        # print("- " * 30)
        if files:
            for file in files:
                abs_path = os.path.join(root, file)
                i = abs_path.index(base_name)
                # print(i)
                name = abs_path[i:].replace("\\", "/")
                files_to_upload.append((abs_path, name))

    # 确保 URL 结尾没有斜杠
    if url.endswith('/'):
        url = url[:-1]

    # 创建一个空的文件列表
    files_list = []
    file_obj_ls = []
    try:
        # 将文件添加到文件列表中
        for file_abs_path, name in files_to_upload:
            file_obj = open(file_abs_path, 'rb')
            # 将文件添加到文件列表
            print(f"name={name}")
            files_list.append(('file', (name, file_obj, 'application/octet-stream')))  # 'file' 是后端获取文件列表的字段
            file_obj_ls.append(file_obj)

        # 创建 MultipartEncoder
        multipart_data = MultipartEncoder(fields=files_list)
        print("文件个数", len(files_list))

        # 设置请求头，指定 MultipartEncoder 的 Content-Type
        headers = {
            'Content-Type': multipart_data.content_type,
            'Authorization': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoZW50aWNhdGVkIjp0cnVlLCJleHAiOjE2OTE2NDE4MjEsInVzZXJfaWQiOjEsInVzZXJfbmFtZSI6ImFkbWluIn0.Hr6htY1t3AxRsWRCRAZ_R3D5_2Zp6TA6YXU-pGpIpvM",
            'Describe-Machine-Code': '3',
            'Describe-Machine-Name': 'MatrixSemi',
        }

        # 发送 POST 请求，上传文件
        response = requests.post(url, data=multipart_data, headers=headers)

        if response.status_code == 200:
            print("Successfully uploaded files to the server.")
        else:
            print(f"Failed to upload files. Status code: {response.status_code}")
    except Exception as e:
        print(f"error: {e}")
    finally:
        for file_obj in file_obj_ls:
            file_obj.close()


if __name__ == "__main__":
    # 替换为你的服务器 URL 和本地目录路径
    server_url = "http://10.0.2.20:8056//api/task/uploadFile"
    local_image_directory = "E:\\Matrixtime\\工作交接20220420\\白路-ADC5000\\接手后-资料\\5000对接6000\\wafer_data_20230313\\Px1002"
    # local_image_directory = "D:\\ADC Data\\TIH2108350"
    upload_files_to_server(server_url, local_image_directory)

    # x = "Px1002"
    # filename = '123.jpeg'
    # p = os.path.join(x, filename)
    # print(f"p = {p}")
    # linux_path = os.path.normpath(p)
    # print(f"linux_path = {linux_path}")
