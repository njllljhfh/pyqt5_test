# -*- coding:utf-8 -*-
import os
import paramiko


class SSH(object):
    def __init__(self, host=None, port=22, user=None, pwd=None):
        self.host = host
        self.user = user
        self.port = port
        self.pwd = pwd
        # private_key_file = '/home/mc5k/.ssh/id_rsa'
        # private_key = paramiko.RSAKey.from_private_key_file(private_key_file)
        try:
            # 建立连接
            self.ssh_client = paramiko.SSHClient()  # 创建sshclient
            # 指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(self.host, port=self.port, username=self.user, password=self.pwd)
            # self.ssh_client.connect(self.host, port=port, username='dev', pkey=private_key)
        except Exception as error:
            print(f"{error}")
            raise

    def close(self):
        self.ssh_client.close()

    def send_command(self, command):
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command)
            out = stdout.readlines()
            err = stderr.readlines()
            return out, err
        except Exception as error:
            print(f"{error}")
            raise


if __name__ == '__main__':
    data_root_dir = '/home/mc5k/sharedir/192.168.10.101/adc5000/changdian'

    # source_dir = '/home/dev/adc5000/data/changdian/TIH2449540/2AI08K9M1/B222449540-01A0'
    source_dir = '/home/dev/adc5000/data/changdian/TIH2449540/2AI08K9M1/B222449540-02G6'
    print(f'source_dir = {source_dir}')

    my_ssh = SSH(host="192.168.10.101", port=22, user="dev", pwd="YzE4ZGY4MzNiMGUzOWIwODhkZDI0M2Mz")
    out, err = my_ssh.send_command(f'chmod -R 777 {source_dir}')
    print(out)
    print(err)
    my_ssh.close()
