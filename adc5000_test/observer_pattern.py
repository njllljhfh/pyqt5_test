# -*- coding:utf-8 -*-
from __future__ import annotations

import os
import shutil
import stat
import time
from multiprocessing import Process
from typing import List

import paramiko
import redis

REDIS_HOST = '10.0.2.20'
REDIS_PORT = 6379
REDIS_CNN = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=1, decode_responses=True)
StopRedisClient = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=5)
STOP_FLAG = 'stop'  # 任务结束符

QUEUE_MAX_LENGTH = 5  # 消息队列最大容量
TRAVERSAL_INTERVAL_TIME = 3  # 根目录遍历的间隔时间（秒）
QUERY_QUEUE_LENGTH_INTERVAL_TIME = 1  # 队列长度查询的间隔时间（秒）

""" ============================== 接口、抽象类 =============================="""


# 观察者接口
class InterfaceObserver(object):
    def report(self, observable: AbstractObservable, data):
        """
        上报数据给上层应用
        :param observable: 被观察者
        :param data: 要传递的数据对象。由被观察者生成，由观察者上报给上层应用。
        :return:
        """
        raise NotImplementedError()


# 被观察者抽象类
class AbstractObservable(object):
    def __init__(self):
        # 所有的观察者
        self._observerList: List[InterfaceObserver] = []

    def add_observer(self, observer: InterfaceObserver):
        """添加观察者"""
        self._observerList.append(observer)

    def delete_observer(self, observer: InterfaceObserver):
        """删除观察者"""
        self._observerList.remove(observer)

    def notify_observers(self, data):
        """通知所有观察者"""
        for observer in self._observerList:
            observer.report(self, data)


# 被观察者-文件监控-抽象类
class AbstractFileMonitor(object):
    def __init__(self, root_dir):
        """
        :param root_dir: 算法服务器，用户wafer数据的挂载点
        """
        self.root_dir = root_dir

    def watch_dir(self):
        """监控指定目录"""
        raise NotImplementedError()


""" ============================== 具体类 =============================="""


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


# 长电被观察者（目录）
class ChangDianFileMonitor(AbstractObservable, AbstractFileMonitor, Process):

    def __init__(self, root_dir, task_id, source_dir, host, port=22, user='', pwd=''):
        """
        :param root_dir:
        :param task_id: 任务id
        :param source_dir: 客户服务器数据所在的目录
        :param host:
        :param port:
        :param user:
        :param pwd:
        """
        super(ChangDianFileMonitor, self).__init__()
        super(AbstractObservable, self).__init__(root_dir)
        super(AbstractFileMonitor, self).__init__()
        self.source_dir = source_dir
        self._is_stopped = False
        self._task_id = task_id
        self._log_pre = f'[Producer  ] 任务【{self._task_id}】'
        self._ssh = None
        self._host = host
        self._port = port
        self._user = user
        self._pwd = pwd

    def run(self):
        self.watch_dir()

    def stop(self):
        self._is_stopped = True

    def watch_dir(self):
        # 监控数据根目录
        try:
            self._ssh = SSH(host=self._host, port=self._port, user=self._user, pwd=self._pwd)
            while not self._is_stopped:
                print(f'{self._log_pre}新一轮监控开始，目录:【{self.root_dir}】')
                wafer_count = self._walk_dir(self.root_dir)
                print(f'{self._log_pre}本轮监控结束，获取到的【数据完整的wafer目录】的个数:{wafer_count}')
                print(f'{self._log_pre}=========================================================================')

                if not self._is_stopped:
                    time.sleep(TRAVERSAL_INTERVAL_TIME)
        except Exception as e:
            raise e
        finally:
            if self._ssh is not None:
                self._ssh.close()

    def _walk_dir(self, root_dir):
        # 此次遍历根目录，获取到的数据完整的 wafer 目录的个数
        wafer_count = 0

        if self._is_stopped:
            return wafer_count

        for root, dirs, files in os.walk(root_dir):
            img_num_in_klarf_file = 0
            img_num_in_root_dir = 0
            has_klarf = False
            for file in files:
                if file.endswith('.klarf'):
                    has_klarf = True
                    klarf_file_path = os.path.join(root, file)
                    # print(f'{self._log_pre}klarf_file_path:【{klarf_file_path}】')
                    with open(klarf_file_path, 'r') as f:
                        line_data = f.readline()
                        while line_data:
                            line_data = line_data.strip()
                            # print(f'{self._log_pre}line_data:【{line_data}】')
                            if line_data.endswith(('.jpg;', '.jpeg;')):
                                img_num_in_klarf_file += 1
                            line_data = f.readline()
                elif file.endswith(('.jpg', '.jpeg')):
                    img_num_in_root_dir += 1

            if has_klarf:
                # print(f'{self._log_pre}img_num_in_klarf_file={img_num_in_klarf_file}')
                # print(f'{self._log_pre}img_num_in_root_dir={img_num_in_root_dir}')
                if img_num_in_klarf_file == img_num_in_root_dir:
                    wafer_count += 1

                    # todo: 将 wafer 数据持久化到数据库中，避免文件目录资源竞争
                    time.sleep(2)  # test: 模拟上传数据耗时

                    # 数据持久化成功后，删除 wafer 文件夹
                    # self._remove_dir(root)

                    # 将新 wafer_dir 通知 观察者
                    self.notify_observers(root)  # test
                    # todo: 发送 wafer_id
                    # self.notify_observers(wafer_id)

            # 监测任务是否停止
            stop_flag = StopRedisClient.get(self._task_id)
            if stop_flag:
                stop_flag = stop_flag.decode('utf-8')
                print(f'{self._log_pre}【停止】监测到结束key:【{stop_flag}】,结束对目录【{self.root_dir}】的监控！')
                self._is_stopped = True
                self.notify_observers(STOP_FLAG)  # 发送任务结束符，通知消费者停止消费
                break

            if (not has_klarf) and dirs:
                for sub_dir in dirs:
                    wafer_count += self._walk_dir(sub_dir)

        return wafer_count

    def _remove_dir(self, dir_path: str):
        print(f'{self._log_pre}删除文件夹:【{dir_path}】')
        source_path = dir_path.replace(self.root_dir, self.source_dir)
        print(f'{self._log_pre}删除文件夹 source_path:【{source_path}】')

        # out, err = self._ssh.send_command(f'chmod -R 777 {source_path}')
        # print(f'{self._log_pre} ssh-chmod-out: {out}')
        # print(f'{self._log_pre} ssh-chmod-err: {err}')

        if source_path != '/':
            out, err = self._ssh.send_command(f'rm -r {source_path}')
            # print(f'{self._log_pre}ssh-rm-out: {out}')
            if err:
                print(f'{self._log_pre}ssh-rm-err: {err}')

            # shutil.rmtree(dir_path)
        else:
            raise ValueError(f'source_path 为系统根目录：【{source_path}】')


# 长电观察者
class ChangDianObserver(InterfaceObserver):

    def __init__(self, task_id, msg_ls_key):
        self._task_id = task_id
        self._msg_ls_key = msg_ls_key
        self._log_pre = f'[P-Observer] 任务【{self._task_id}】'

    def report(self, observable: AbstractObservable, data):
        # print(f'{self._log_pre}观察到具有完整数据的wafer目录。。。')
        self._send_data_to_queue(data)

    def _send_data_to_queue(self, data):
        if data == STOP_FLAG:
            print(f'{self._log_pre}发送结束符【{data}】到消息队列【{self._msg_ls_key}】')
            REDIS_CNN.rpush(self._msg_ls_key, data)
        else:
            # 判断队列长度
            queue_length = REDIS_CNN.llen(self._msg_ls_key)
            while queue_length >= QUEUE_MAX_LENGTH:
                print(f'{self._log_pre}消息队列【{self._msg_ls_key}】中的数据个数已满，当前的数据个数为:{queue_length}')
                time.sleep(QUERY_QUEUE_LENGTH_INTERVAL_TIME)
                queue_length = REDIS_CNN.llen(self._msg_ls_key)

            # 发送新目录到redis的列表
            # print(f'{self._log_pre}发送新 wafer 数据【{data}】到消息队列【{self._msg_ls_key}】')
            REDIS_CNN.rpush(self._msg_ls_key, data)


class Consumer(Process):
    def __init__(self, msg_ls_key, task_id):
        super().__init__()
        self._msg_ls_key = msg_ls_key
        self._task_id = task_id
        self._is_stopped = False
        self._log_pre = f'[Consumer  ] 任务【{self._task_id}】'

    def run(self) -> None:
        while not self._is_stopped:
            try:
                data_package = REDIS_CNN.blpop(self._msg_ls_key, 0)
                data = data_package[1]  # 生产环境下是 wafer_id

                if data == STOP_FLAG:
                    self._is_stopped = True
                    StopRedisClient.delete(self._task_id)
                    print(f'{self._log_pre}监测到结束符:【{data}】, 消费结束！')
                    break
                else:
                    print(f'{self._log_pre}获取到新 wafer 数据:【{data}】')
                    time.sleep(3)  # test:模拟检测一个wafer的耗时
            except Exception as e:
                raise e

    # def run(self) -> None:
    #     while not self._is_stopped:
    #         try:
    #             data_package = REDIS_CNN.lpop(self._msg_ls_key)
    #             if data_package:
    #                 data = data_package[1]  # 生产环境下是 wafer_id
    #
    #                 if data == STOP_FLAG:
    #                     self._is_stopped = True
    #                     StopRedisClient.delete(self._task_id)
    #                     print(f'{self._log_pre}监测到结束符:【{data}】, 消费结束！')
    #                     break
    #                 else:
    #                     print(f'{self._log_pre}获取到新 wafer 数据:【{data}】')
    #                     time.sleep(3)  # test:模拟检测一个wafer的耗时
    #             else:
    #                 time.sleep(0.01)
    #         except Exception as e:
    #             raise e

    def stop(self):
        self._is_stopped = True


"""============================== 场景类（测试） =============================="""


# 场景类
class Client(object):

    @staticmethod
    def main():
        # todo: 新建任务
        pass
        task_id = 1314520
        msg_ls_key = f'atq_{task_id}'  # atp: auto task queue

        # 客户观察者
        chang_dian_observer = ChangDianObserver(task_id, msg_ls_key)

        # 客户被观察者
        host = "192.168.10.101"
        port = 22
        user = "dev"
        pwd = "YzE4ZGY4MzNiMGUzOWIwODhkZDI0M2Mz"
        # data_root_dir = 'D:\\ADC Data'  # 客户被监控目录
        data_root_dir = '/home/mc5k/sharedir/192.168.10.101/adc5000/changdian'  # 被监控目录(AI服务器上的挂载点）
        source_dir = '/home/dev/adc5000/data/changdian'  # 客户自己的linux服务器上的源文件目录
        chang_dian_file_monitor = ChangDianFileMonitor(
            data_root_dir, task_id, source_dir, host, port=port, user=user, pwd=pwd
        )
        chang_dian_file_monitor.add_observer(chang_dian_observer)

        # 启动文件监控
        StopRedisClient.delete(task_id)
        REDIS_CNN.delete(msg_ls_key)
        chang_dian_file_monitor.start()
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # 检测进程(celery)
        detection_process = Consumer(msg_ls_key, task_id)
        detection_process.start()

        print(f'任务【{task_id}】【开始】成功！')


if __name__ == '__main__':
    client = Client()
    client.main()
