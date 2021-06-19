# -*- coding:utf-8 -*-
# __author__ = "Dragon"
import argparse
import os
import re
import shutil
import time
import ftplib
from ftplib import FTP
from io import BytesIO
import numpy as np


class ImageCollector(object):

    def __init__(self, source_path: str, export_path: str, loop_number=None, interval=None):
        self.source_path = source_path
        self.export_path = export_path
        self.loop_number = loop_number
        self.interval = interval or 5

        self.ftp = FtpImage(file_path=source_path)

        print(f"source_path={self.source_path}, type(source_path)={type(self.source_path)}")
        print(f"export_path={self.export_path}, type(export_path)={type(self.export_path)}")
        print(f"loop_number={self.loop_number}, type(loop_number)={type(self.loop_number)}")
        print(f"interval={self.interval}, type(interval)={type(self.interval)}")

    def export_images(self, flag='vi'):
        if self.loop_number:
            total_time = self.loop_number * self.interval
        else:
            total_time = 1

        consumed_time = 0
        pattern = r'^%s(\d+)_([A-Za-z\d]+)\.(.*)' % flag
        prefix = f"{flag}"

        self._clear_path()

        export_product_code = 1
        product_num_previous = None  # The code of previous product exported from source directory.

        while (self.loop_number is None) or (consumed_time < total_time):
            try:
                print(f"consumed_time={consumed_time}")
                time.sleep(self.interval)
                consumed_time += self.interval

                # for root, dirs, files in os.walk(self.source_path):
                files = self.ftp.get_file_list()
                if not len(files):
                    continue
                # - - -
                print(f"file list = {files}")

                product_num_ls = list()
                name_without_suffix_ls = list()
                for file_name in files:
                    res = re.search(pattern, file_name)
                    product_num = res.group(1)  # ex. 8
                    product_num_ls.append(int(product_num))
                    name_without_suffix = file_name.split(".")[0]  # ex. vi2_B3
                    name_without_suffix_ls.append(name_without_suffix)

                product_num_ls = list(set(product_num_ls))
                # The code of product being exported from the source directory.
                product_num_current = min(product_num_ls)
                # - - -

                # If the images of the first product is not complete, delete all images of it.
                source_img_prefix = f"{flag}{product_num_current}"
                A1 = f"{source_img_prefix}_A1"
                print(f"name_without_suffix_ls = {name_without_suffix_ls}")
                if product_num_previous is None:
                    if A1 in name_without_suffix_ls:
                        pass
                    else:
                        for source_img_name in files:
                            if source_img_name.startswith(source_img_prefix):
                                # source_img_path = os.path.join(root, source_img_name)
                                # print(f"Delete image of incomplete product. --- {source_img_path}")
                                # os.remove(source_img_path)
                                self.ftp.delete_file(source_img_name)
                                print(f"Delete image of incomplete product. --- {source_img_name}")
                        continue
                # - - -

                # print(f"product_num_ls = {product_num_ls}")
                print(f"product_num_previous = {product_num_previous}")
                print(f"product_num_current = {product_num_current}")
                if product_num_previous is None:
                    product_num_previous = product_num_current

                if product_num_current != product_num_previous:
                    product_num_previous = product_num_current
                    export_product_code += 1
                # - - -

                # Export image and delete source image.
                for source_img_name in files:
                    if source_img_name.startswith(flag + f"{product_num_current}_"):
                        # source_img_path = os.path.join(root, source_img_name)

                        res = re.search(pattern, source_img_name)
                        img_part = res.group(2)  # ex. A1
                        img_type = res.group(3)  # ex. jpg
                        # print(source_img_path, " ", img_part)
                        # - - -

                        export_img_name = f"{prefix}{export_product_code}_{img_part}.{img_type}"
                        export_img_path = os.path.join(self.export_path, export_img_name)
                        # print(f"{export_img_path}")
                        # print("-" * 10)

                        # with open(source_img_path, "rb") as export_f:
                        #     content = export_f.read()
                        # # Export image.
                        # with open(export_img_path, "wb") as export_f:
                        #     export_f.write(content)
                        content = self.ftp.read_file(source_img_name)
                        with open(export_img_path, "wb") as export_f:
                            export_f.write(content)

                        # Delete source image.
                        # os.remove(source_img_path)
                        self.ftp.delete_file(source_img_name)
            except KeyboardInterrupt:
                print("KeyboardInterrupt")
                self.ftp.close_connection()
                return
            except ftplib.Error as e:
                print(f"Error: {e}  ErrorType:{type(e)}")
                self.ftp.close_connection()
                self.ftp.connect_and_login()
            except Exception as e:
                print(f"Error: {e}")
                self.ftp.close_connection()
                self.ftp.connect_and_login()

    def _clear_path(self):
        # for root, dirs, files in os.walk(self.source_path):
        #     # Delete files.
        #     for f in files:
        #         os.remove(os.path.join(root, f))

        #     # Delete folders.
        #     for d in dirs:
        #         shutil.rmtree(os.path.join(root, d))
        files = self.ftp.get_file_list()
        for file_name in files:
            self.ftp.delete_file(file_name)


class FtpImage(object):

    def __init__(self, addr="10.0.1.9", port=21, user='admin', pwd="123456", file_path="/APP/testimg/"):
        self.addr = addr
        self.port = port
        self.user = user
        self.pwd = pwd
        self.file_path = file_path

        self.ftp = FTP()
        self.connect_and_login()

        # Switch to target directory.
        self.ftp.cwd(self.file_path)

    def connect_and_login(self):
        self.ftp.connect(self.addr, self.port)
        self.ftp.login(self.user, self.pwd)

    def get_file_list(self):
        self.ftp.cwd(self.file_path)
        return self.ftp.nlst()

    def read_file(self, file_name):
        # with open(save_file, "wd") as file_handle:
        self.ftp.cwd(self.file_path)
        img_bytes = BytesIO()
        self.ftp.retrbinary(f'RETR {file_name}', img_bytes.write)
        image = np.asarray(bytearray(img_bytes.getbuffer()), dtype='uint8')
        return image

    def delete_file(self, file_name):
        self.ftp.cwd(self.file_path)
        self.ftp.delete(file_name)

    def close_connection(self):
        self.ftp.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source-path', dest='source_path', type=str, default=None, required=True,
                        help='Source path of images.')
    parser.add_argument('-o', '--export-path', dest='export_path', type=str, default=None, required=True,
                        help='Export path of images.')
    parser.add_argument('-lp', '--loop-number', dest='loop_number', type=int, default=None, required=False,
                        help='Number of loops. If this argument is not set, the loop of exporting image will not stop.')
    parser.add_argument('-i', '--interval', dest='interval', type=float, default=None, required=False,
                        help='The sleeping time of each loop.')

    args = parser.parse_args()

    source_path = args.source_path
    export_path = args.export_path
    loop_number = args.loop_number
    interval = args.interval

    image_collector = ImageCollector(source_path, export_path, loop_number=loop_number, interval=interval)
    image_collector.export_images(flag='vi')

    """
    Usage:
        > python3 image_collector_atesi.py -s /APP/testimg/ -o ./image_collector_atesi_vi_export
        
    Usage for daemon process:
        > nohup python3 -u image_collector_atesi.py -s /APP/testimg/ -o ./image_collector_atesi_vi_export >> image_collector.log 2>&1 &
    """
