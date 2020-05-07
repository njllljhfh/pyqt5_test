# -*- coding:utf-8 -*-
from collections import OrderedDict

xxx = {2587: {'product_id': 2587, 'product_code': '1', 'inference_result': 0,
              'received_img_step_el': ['TP1', 'TP2', 'TP3'], 'received_img_step_vi': [],
              'received_defect_step_el': ['TP1', 'TP2', 'TP3'], 'received_defect_step_vi': [],
              'defect_intelligent_el': {
                  'TP1': [
                      {'box': [8, 502, 93, 56],
                       'roi': [5365, 707, 295, 584],
                       'score': 0.9999977350234985,
                       'class_order_id': 4,
                       'position': [2, 18],
                       'angle': None,
                       'class_name': '虚焊',
                       'defect_level': 0},
                      {'box': [8, 447, 96, 52],
                       'roi': [5365, 707, 295, 584],
                       'score': 0.9995397329330444,
                       'class_order_id': 4, 'position': [2, 18], 'angle': None, 'class_name': '虚焊', 'defect_level': 0}],
                  'TP2': [
                      {'class_order_id': 102,
                       'roi': None,
                       'score': None,
                       'class_name': '拼接不良',
                       'defect_level': 1}
                  ],
                  'TP3': [
                      {
                          'box': [151, 26, 136, 59],
                          'roi': [2250, 2605, 306, 583],
                          'score': 0.9986855387687683,
                          'class_order_id': 4,
                          'position': [5, 8],
                          'angle': None,
                          'class_name': '虚焊',
                          'defect_level': 0
                      },
                      {
                          'box': [11, 443, 83, 52],
                          'roi': [5368, 3188, 294, 582],
                          'score': 0.999983549118042,
                          'class_order_id': 4,
                          'position': [6, 18],
                          'angle': None, 'class_name': '虚焊',
                          'defect_level': 0
                      },
                      {
                          'box': [11, 494, 75, 62],
                          'roi': [5368, 3188, 294, 582],
                          'score': 0.9090363383293152,
                          'class_order_id': 4,
                          'position': [6, 18],
                          'angle': None,
                          'class_name': '虚焊',
                          'defect_level': 0
                      },
                      {
                          'box': [196, 31, 98, 59],
                          'roi': [5662, 3188, 295, 582],
                          'score': 0.9976656436920166,
                          'class_order_id': 4,
                          'position': [6, 19],
                          'angle': None,
                          'class_name': '虚焊',
                          'defect_level': 0
                      },
                      {
                          'box': [163, 31, 116, 54],
                          'roi': [5970, 3191, 284, 576],
                          'score': 0.9999972581863403,
                          'class_order_id': 4,
                          'position': [6, 20],
                          'angle': None,
                          'class_name': '虚焊',
                          'defect_level': 0
                      }
                  ]
              },
              'defect_intelligent_vi': {'TP1': [], 'TP2': [], 'TP3': []}}}

if __name__ == '__main__':
    a_dict = OrderedDict()

    a_dict["xxx"] = "hello_1"
    a_dict["yyy"] = "hello_2"

    a_dict.pop("xxx")

    print(a_dict)
