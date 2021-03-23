# -*- coding:utf-8 -*-
task_machine_id_ls = [1, 2, 3, 4, 5, 6]
for i, task_machine_id in enumerate(task_machine_id_ls):
    row = int(i / 3)
    column = i % 3
    print(f'row={row}, column={column}')
