# -*- coding:utf-8 -*-


def xxx():
    try:
        pass
        return print(1)
    except Exception as e:
        pass
        print(e)
    finally:
        print(f"finally")



if __name__ == '__main__':
    xxx()
