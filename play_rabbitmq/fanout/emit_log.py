# -*- coding:utf-8 -*-
import pika
import random
import time
from datetime import datetime

VHOST = 'adcvhost'
NODE1_ADDR = '10.211.55.10:5672'
NODE2_ADDR = '10.211.55.11:5672'
NODE3_ADDR = '10.211.55.12:5672'

node1 = pika.URLParameters(f'amqp://admin:admin@{NODE1_ADDR}/{VHOST}')
node2 = pika.URLParameters(f'amqp://admin:admin@{NODE2_ADDR}/{VHOST}')
node3 = pika.URLParameters(f'amqp://admin:admin@{NODE3_ADDR}/{VHOST}')

all_endpoints = [node1, node2, node3]

random.shuffle(all_endpoints)

is_disconnected = True

print("生产者: 首次连接...")
while is_disconnected:
    for url in all_endpoints:
        try:
            connection = pika.BlockingConnection(url)
            is_disconnected = False
        except Exception as e:
            print(f'url连接失败：{url.host}')
            continue

        try:
            print(f'url = {url.host}')
            channel = connection.channel()
            channel.basic_qos(prefetch_count=1)

            channel.exchange_declare(exchange='logs', exchange_type='fanout')

            while True:
                message = f'info: Hello World!-{datetime.now()}'
                channel.basic_publish(exchange='logs', routing_key='', body=message)
                print(f" [x] Sent {message}")
                time.sleep(1.5)
        except Exception as e:
            connection.close()
            is_disconnected = True
            print(f'生产过程中报错：{e}')
            break

    print("生产者: 重新连接...")
