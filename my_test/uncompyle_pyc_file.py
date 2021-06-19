# encoding=utf8
import os
import uncompyle6


def main():
    path = 'C:\\Users\\Administrator\\Desktop\\xxx'
    for root, dirs, files in os.walk(path):
        if root != path:
            break
        for filename in files:
            if filename.endswith('pyc'):
                print(filename)
                new_py = filename.split('.')[0] + ".py"
                new_path = path + '\\' + new_py
                print(f"new_path = {new_path}")
                with open(f"{new_path}", "w", encoding='utf8') as f:
                    uncompyle6.decompile_file(path + '\\' + filename, f)


if __name__ == '__main__':
    main()
