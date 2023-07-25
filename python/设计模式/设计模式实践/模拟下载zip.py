# -*- coding:utf-8 -*-
import requests


def download_zip(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查是否有错误的响应

        with open(save_path, 'wb') as file:
            file.write(response.content)

        print("Download successful. Zip file saved as:", save_path)
    except requests.exceptions.RequestException as e:
        print("Error occurred during download:", e)


if __name__ == "__main__":
    url = "http://10.0.2.7:7156/api/recheck/exportWaferMetaData?wafer_ids=2"
    save_path = "downloaded_file.zip"

    download_zip(url, save_path)
