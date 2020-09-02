# -*- coding:utf-8 -*-
import fractions
import math


def get_scale_layout_stretch(column, per=4):
    res = column / per
    print("res = {}".format(res))

    horizontal_scale_count: int = math.ceil(res)
    print("horizontal_scale_count = {}".format(horizontal_scale_count))

    # fractional_integer: (float, float) = math.modf(res)
    # print("fractional_integer = {}".format(fractional_integer))
    # decimal_part = fractional_integer[0]
    # if decimal_part == 0:
    #     deci = 1
    # else:
    #     deci = decimal_part

    remainder = column % per  # 余数
    print("remainder = {}".format(remainder))
    if remainder == 0:
        big_factor = 1
        small_factor = 1
    else:
        big_factor = per
        small_factor = remainder

    # if remainder == 0:
    #     fract = fractions.Fraction(1)
    # else:
    #     fract = fractions.Fraction(remainder / per)
    #
    # # print("deci = {}".format(deci))
    #
    # print("fract = {}".format(fract))
    # print("numerator = {}".format(fract.numerator))
    # print("denominator = {}".format(fract.denominator))
    # layout_stretch = [fract.denominator for _ in range(horizontal_scale_count - 1)]
    # layout_stretch.append(fract.numerator)

    layout_stretch = [big_factor for _ in range(horizontal_scale_count - 1)]
    layout_stretch.append(small_factor)

    return layout_stretch, horizontal_scale_count


if __name__ == '__main__':
    column =66
    layout_stretch, horizontal_scale_count = get_scale_layout_stretch(column, per=5)
    print("layout_stretch = {}".format(layout_stretch))
    print("len(layout_stretch) = {}".format(len(layout_stretch)))
    print("horizontal_scale_count = {}".format(horizontal_scale_count))
    print("sum(layout_stretch) = {}".format(sum(layout_stretch)))
    print("sum(layout_stretch)==column: {}".format(sum(layout_stretch) == column))
