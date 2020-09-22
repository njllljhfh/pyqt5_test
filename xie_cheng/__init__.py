# -*- coding:utf-8 -*-


def xxx():
    try:
        print(1)
        a = 1 / 0
        return
    except Exception as e:
        print(f"error = {e}")
    finally:
        print("finally")


if __name__ == '__main__':
    xxx()
