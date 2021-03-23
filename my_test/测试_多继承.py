# -*- coding:utf-8 -*-


class A(object):

    def do_something(self):
        print(f"- - - A - - -")


class B(object):

    def do_something(self):
        print(f"- - - B - - -")


class C(A, B):

    def do_something(self):
        print(f"- - - C - - -")


class E(C):

    def do_something(self):
        print(f"- - - E - - -")


class D(E, C, B):

    def do_something(self):
        print(f"- - - D - - -")


class F(C):

    def do_something(self):
        print(f"- - - F - - -")
        super(A, self).do_something()


if __name__ == '__main__':
    f = F()
    f.do_something()
    print(F.mro())
    print(C.mro())
    print('~  ' * 30)

    # e = E()
    # e.do_something()
    # print(E.mro())
    # print('*  ' * 30)
