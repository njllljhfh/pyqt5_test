# -*- coding:utf-8 -*-
import json
import os

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

# 光伏拼图模块上传图像
# def _http_splicing_image(data: dict, local_directory, timeout=30):
#     """
#     此方式废弃
#     此方法用于http请求，通过web表单上传图像和拼图参数给后端服务
#     :param data: 拼图参数
#     :param local_directory: 本地图像目录的绝对路径
#     :param timeout: 本地图像目录的绝对路径
#     :return:
#     """
#     # url = "http://127.0.0.1:8000/api/task/uploadFile"
#     url = "http://ip:port/xxx..."
#
#     base_name = os.path.basename(local_directory)
#     logger.info(f"base_name = {base_name}")
#
#     files_to_upload = []
#     for root, dirs, files in os.walk(local_directory):
#         # print(f"root = {root}")
#         # print(f"dirs = {dirs}")
#         # print(f"files = {files}")
#         # print("- " * 30)
#         if files:
#             for file in files:
#                 abs_path = os.path.join(root, file)
#                 i = abs_path.index(base_name)
#                 name = abs_path[i:].replace("\\", "/")
#                 files_to_upload.append((abs_path, name))
#
#     files_list = []
#     file_obj_ls = []
#     try:
#         for file_abs_path, name in files_to_upload:
#             file_obj = open(file_abs_path, 'rb')
#             logger.info(f"file={name}")
#             files_list.append(('file', (name, file_obj, 'application/octet-stream')))  # 'file' 是后端获取文件列表的字段
#             file_obj_ls.append(file_obj)
#
#         multipart_data = MultipartEncoder(fields=files_list)
#         logger.info(f"文件个数: {len(files_list)}")
#
#         headers = {
#             'Content-Type': multipart_data.content_type,
#             'StitchingData': json.dumps(data),
#             # 'Authorization': "",
#         }
#         response = requests.post(url, data=multipart_data, headers=headers, timeout=timeout)
#
#         if response.status_code == 200:
#             logger.info("上传图像，拼图成功")
#             img_bytes = response.content
#             return img_bytes
#         else:
#             logger.info(f"上传图像，拼图失败，Status code:{response.status_code}")
#     except Exception as e:
#         msg = f"上传图像，拼图异常，error: {e}"
#         logger.error(msg, exc_info=True)
#         raise ValueError(f"拼图失败或超时(timeout: {timeout}s)")
#     finally:
#         for file_obj in file_obj_ls:
#             file_obj.close()


"""
模拟web表单，上传本地目录中的全部文件
"""


def upload_files_to_server(url, local_directory):
    base_name = os.path.basename(local_directory)
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

        stitching_data = {
            "rect_ls": [[[463.27077747989273, 164.71849865951742], [1647.1849865951742, 952.278820375335]],
                        [[433.5483870967742, 160.0], [1651.6129032258063, 949.6774193548387]],
                        [[293.4048257372654, 149.27613941018765], [1477.3190348525468, 952.278820375335]],
                        [[278.7096774193548, 160.0], [1450.3225806451615, 944.516129032258]],
                        [[468.4182305630027, 169.86595174262735], [1642.0375335120643, 947.1313672922251]],
                        [[454.19354838709677, 165.16129032258064], [1641.2903225806451, 944.516129032258]],
                        [[303.69973190348526, 164.71849865951742], [1467.024128686327, 941.9839142091153]],
                        [[485.1612903225806, 160.0], [1651.6129032258063, 944.516129032258]],
                        [[468.4182305630027, 164.71849865951742], [1647.1849865951742, 957.426273458445]],
                        [[454.19354838709677, 175.48387096774192], [1651.6129032258063, 954.8387096774193]],
                        [[298.5522788203753, 164.71849865951742], [1482.466487935657, 957.4262734584452]],
                        [[281.5292762001515, 163.1444862128241], [1455.483870967742, 949.6774193548387]]]}
        # 设置请求头，指定 MultipartEncoder 的 Content-Type
        headers = {
            'Content-Type': multipart_data.content_type,
            'Authorization': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoZW50aWNhdGVkIjp0cnVlLCJleHAiOjE2OTMyNzM2MDEsInVzZXJfaWQiOjEsInVzZXJfbmFtZSI6ImFkbWluIn0.rV6E-7brnh0heMC1HlyHi7Mx5t93o2XABmMh5PkHDPU",
            'Describe-Machine-Code': '3',
            'Describe-Machine-Name': 'MatrixSemi',
            'StitchingData': json.dumps(stitching_data),
        }

        # 发送 POST 请求，上传文件
        response = requests.post(url, data=multipart_data, headers=headers)

        if response.status_code == 200:
            # 如果返回的是图像，获取图像二进制数据
            # img_data = response.content
            # with open("./xxx.jpg", "wb") as f:
            #     f.write(img_data)
            print("Successfully uploaded files to the server.")
        else:
            print(f"Failed to upload files. Status code: {response.status_code}")
    except Exception as e:
        print(f"error: {e}")
    finally:
        for file_obj in file_obj_ls:
            file_obj.close()


# def post(self, request):
#     """拼图"""
#     from django.utils.encoding import escape_uri_path
#     from django.http import HttpResponse
#     file_ls = request.FILES.getlist("file")
#     stitching_data = request.headers.get("StitchingData", None)
#     logger.info(f"stitching_data = {type(stitching_data)}")
#     if stitching_data:
#         stitching_data = json.loads(stitching_data)
#         logger.info(f"stitching_data={stitching_data}")
#     filename = f'full_image.jpg'
#     img_path = 'E:\\Matrixtime\\workfile\\GitHub\\pyqt5_test\\images\\EL_TP3.jpg'
#     with open(img_path, "rb") as f:
#         img_bytes = f.read()  # TODO：替换为算法返回的整图二进制数据
#     response = HttpResponse(img_bytes)
#     response["Content-Type"] = "application/octet-stream"
#     response["Content-Disposition"] = "attachment; filename={}".format(escape_uri_path(filename))
#     return response


if __name__ == "__main__":
    # 替换为你的服务器 URL 和本地目录路径
    # server_url = "http://10.0.2.20:8056//api/task/uploadFile"
    server_url = "http://127.0.0.1:8000/api/task/uploadFile"
    local_image_directory = "E:\\Matrixtime\\工作交接20220420\\白路-ADC5000\\接手后-资料\\5000对接6000\\wafer_data_20230313\\Px1002"
    # local_image_directory = "D:\\ADC Data\\TIH2108350"
    upload_files_to_server(server_url, local_image_directory)

    # x = "Px1002"
    # filename = '123.jpeg'
    # p = os.path.join(x, filename)
    # print(f"p = {p}")
    # linux_path = os.path.normpath(p)
    # print(f"linux_path = {linux_path}")
