# -*- coding:utf-8 -*-
import time


def main():
    i = 1
    try:
        while True:
            print(i)
            time.sleep(0.5)
            i += 1
            if i == 3:
                a = 1 / 0
    except Exception as e:
        print(f'Error: {e}')


def main2():
    i = 1
    while True:
        try:
            print(i)
            time.sleep(0.5)
            i += 1

            if i == 8:
                return

            if i % 2 == 0:
                a = 1 / 0
        except Exception as e:
            print(f'Error: {e}')


def main3():

    for i in range(10):
        print(i)
        if i == 9:
            # pass  # else 会执行
            break  # else 不会执行
    else:
        print(f'else')


def main4():
    """while循环内不捕捉异常，while循环会退出。"""
    i = 1
    while True:
        print(i)
        time.sleep(0.5)
        i += 1

        if i == 8:
            return

        if i % 2 == 0:
            a = 1 / 0


if __name__ == '__main__':
    # main()

    # main2()

    # main3()

    main4()
