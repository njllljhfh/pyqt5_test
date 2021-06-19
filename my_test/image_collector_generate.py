# -*- coding:utf-8 -*-


def create_image(folder: str, source_file_name: str):
    with open(folder + "\\" + source_file_name, "rb") as f:
        content = f.read()

        product = source_file_name.split('.')[0]
        print(f"product={product}")
        for i in range(0, 3):
            for j in range(1, 5):
                new_file_path = folder + "\\" + f"vi{product}_{chr(65 + i)}{j}" + ".png"
                print(new_file_path)
                with open(new_file_path, "wb") as f1:
                    f1.write(content)


if __name__ == '__main__':
    create_image('C:\\Users\\Administrator\\Desktop\\新建文件夹', '8.png')
