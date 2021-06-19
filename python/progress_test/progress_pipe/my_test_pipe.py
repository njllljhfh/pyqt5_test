# -*- coding:utf-8 -*-
from multiprocessing import Pipe
from multiprocessing import connection

# a, b = Pipe()
# a.send([1, 'hello', None])
# print(b.recv())
# [1, 'hello', None]
# b.send_bytes(b'thank you')
# print(a.recv_bytes())
# # b'thank you'
# import array
#
# arr1 = array.array('i', range(5))
# arr2 = array.array('i', [0] * 10)
# print(f'arr2={arr2}')
# a.send_bytes(arr1)
# count = b.recv_bytes_into(arr2)
# print(f'count = {count}')
# print(f'len(arr1) = {len(arr1)}')
# print(f'arr1.itemsize = {arr1.itemsize}')
# assert count == len(arr1) * arr1.itemsize
# print(f"arr2 = {arr2}")
# # array('i', [0, 1, 2, 3, 4, 0, 0, 0, 0, 0])
# arr3 = array.array('i', range(21, 30))
# print(arr3)
# a.send_bytes(arr3)
# count = b.recv_bytes_into(arr2)
# print(f"arr2 = {arr2}")
# print(f'count = {count}')
#
# import os
#
# print(os.urandom(5))
# - - -

w, r = Pipe()
w.send([1, 'hello', None])
r_ls = [r, ]
# Return whether there is any data available to be read.
print('r.poll() =', r.poll())

# Wait till an object in object_list is ready.
# Returns the list of those objects in object_list which are ready.
# If timeout is a float then the call blocks for at most that many seconds.
# If timeout is None then it will block for an unlimited period.
# A negative timeout is equivalent to a zero timeout.
print('connection.wait(r_ls) =', connection.wait(r_ls))

print('r.recv() =', r.recv())
print('r.poll() =', r.poll())
print('connection.wait(r_ls, timeout=0) =', connection.wait(r_ls, timeout=0))
