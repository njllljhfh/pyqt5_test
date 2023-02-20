# -*- coding:utf-8 -*-

class X(object):

    def talk(self):
        print(f'我是 X')


class A(X):

    def talk(self):
        print(f'我是 A')


class B(object):

    def talk(self):
        print(f'我是 B')


class C(A, B):

    def talk(self):
        super().talk()
        super(C, self).talk()

        super(A, self).talk()

        B.talk(self)


if __name__ == '__main__':
    c = C()
    print(C.__mro__)
    c.talk()
