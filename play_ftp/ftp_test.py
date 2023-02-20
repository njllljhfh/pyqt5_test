# -*- coding:utf-8 -*-
from ftplib import FTP
from io import BytesIO

ip = '10.0.1.5'
port = 21


def test_ftp():
    ftp = FTP()
    ftp.connect(ip, port)
    ftp.login('adcUser1', '123')  # 如果是匿名登录，直接ftp.login()
    # print(ftp.getwelcome())  # 打印出欢迎信息

    files = ftp.dir('/')
    print(f'files = {files}')

    # 向ftp服务器写一个文件
    print('向ftp服务器写一个文件')
    ftp.cwd('/')
    f = BytesIO()
    f.write('klarf file gotten'.encode('utf-8'))
    f.seek(0)
    buffer_size = 1024
    remote_path = '/k.txt'
    ftp.storbinary(f'STOR {remote_path}', f, blocksize=buffer_size)
    print('- ' * 30)

    # 从ftp服务器读文件,并在文件末尾追加内容
    print('从ftp服务器读文件,并在文件末尾追加内容')
    f = BytesIO()
    remote_path = '/a1.txt'
    ftp.retrbinary(f'RETR {remote_path}', f.write)
    f.write(f'\r\n222'.encode('utf-8'))
    f.seek(0)
    print(f.getvalue().decode('utf-8'))
    ftp.storbinary(f'STOR {remote_path}', f, blocksize=buffer_size)
    print('- ' * 30)


if __name__ == '__main__':
    test_ftp()
