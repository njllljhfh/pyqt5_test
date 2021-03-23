# -*- coding:utf-8 -*-
from multiprocessing import Pipe

a, b = Pipe()
a.send([1, 'hello', None])
print(b.recv())
# [1, 'hello', None]
b.send_bytes(b'thank you')
print(a.recv_bytes())
# b'thank you'
import array

arr1 = array.array('i', range(5))
arr2 = array.array('i', [0] * 10)
a.send_bytes(arr1)
count = b.recv_bytes_into(arr2)
print(f'count = {count}')
print(f'len(arr1) = {len(arr1)}')
print(f'arr1.itemsize = {arr1.itemsize}')
assert count == len(arr1) * arr1.itemsize
print(f"arr2 = {arr2}")
# array('i', [0, 1, 2, 3, 4, 0, 0, 0, 0, 0])
arr3 = array.array('i', range(21, 30))
print(arr3)
a.send_bytes(arr3)
count = b.recv_bytes_into(arr2)
print(f"arr2 = {arr2}")

import os

print(os.urandom(5))
