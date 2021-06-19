# -*- coding:utf-8 -*-
pro_line_id = [1, 2]
sql = """
        SELECT
            main.*,
            d_t_i.D_TASK_NAME 
        FROM
            TASK_MACHINES AS main
            LEFT JOIN DETECT_TASK_INFO AS d_t_i ON main.D_TASK_ID = d_t_i.D_TASK_ID 
        WHERE
            d_t_i.D_TASK_ID != {d_task_id} 
            AND d_t_i.TASK_OPER_STATUS = {task_oper_status} 
            AND main.PRO_LINE_ID IN ({pro_line_id})
            AND main.DETECT_SITE = {detect_site};
        """.format(d_task_id=2020091448856465927,
                   task_oper_status=1,
                   pro_line_id=','.join(map(str, pro_line_id)),
                   detect_site=1)

print(sql)