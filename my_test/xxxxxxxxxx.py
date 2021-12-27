# -*- coding:utf-8 -*-
import ctypes

print(ctypes.c_ushort(-1))

a = 65535
print('-----')
res = ctypes.c_short(a)
print(res.value)
print(float(res.value))
