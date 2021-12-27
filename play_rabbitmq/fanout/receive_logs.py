# -*- coding:utf-8 -*-
import pika
import random

VHOST = 'adcvhost'
NODE1_ADDR = '10.211.55.10:5672'
NODE2_ADDR = '10.211.55.11:5672'
NODE3_ADDR = '10.211.55.12:5672'

node1 = pika.URLParameters(f'amqp://admin:admin@{NODE1_ADDR}/{VHOST}')
node2 = pika.URLParameters(f'amqp://admin:admin@{NODE2_ADDR}/{VHOST}')
node3 = pika.URLParameters(f'amqp://admin:admin@{NODE3_ADDR}/{VHOST}')

all_endpoints = [node1, node2, node3]

random.shuffle(all_endpoints)


def callback(ch, method, properties, body):
    print(f" [x] {body}")


is_disconnected = True

print("消费者: 首次连接...")
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

            result = channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue

            channel.queue_bind(exchange='logs', queue=queue_name)

            print(' [*] Waiting for logs. To exit press CTRL+C')

            channel.basic_consume(
                queue=queue_name, consumer_callback=callback, no_ack=True)

            channel.start_consuming()
        except Exception as e:
            connection.close()
            is_disconnected = True
            print(f'消费过程中报错：{e}')
            break

    print("消费者: 重新连接...")
