# -*- coding:utf-8 -*-
class CLanguage:
    # 定义__call__方法
    def __call__(self, name, add):
        print("调用__call__()方法", name, add)


print("**********")
clangs = CLanguage()
clangs("C语言中文网", "http://c.biancheng.net")
clangs.__call__("C语言中文网", "http://c.biancheng.net")

print("**********")


def say():
    print("Python教程：http://c.biancheng.net/python")


say()
say.__call__()

print("- " * 30)


class CLanguage:
    def __init__(self):
        self.name = "C语言中文网"
        self.add = "http://c.biancheng.net"

    def say(self):
        print("我正在学Python")


clangs = CLanguage()
if hasattr(clangs, "name"):
    print(hasattr(clangs.name, "__call__"))
print("**********")
if hasattr(clangs, "say"):
    print(hasattr(clangs.say, "__call__"))

print("- " * 30)
