# -*- coding:utf-8 -*-
# 定期1年
one = 1.0165
# 定期2年
two = 1.0205 ** 2
# 定期3年
three = 1.0245 ** 3
# 定期5年
five = 1.025 ** 5

# q = 100000 * five ** 10
# print(q)
#
# # 1 - 5 年
# y = 40000 * (1.025 ** 5 + 1.025 ** 4 + 1.025 ** 3 + 1.025 ** 2 + 1.025 ** 1)
# # 6 - 10 年
# z = y / 5 * (1.025 ** 5 + 1.025 ** 4 + 1.025 ** 3 + 1.025 ** 2 + 1.025 ** 1)
# # 11 - 15 year
# a = z / 5 * (1.025 ** 5 + 1.025 ** 4 + 1.025 ** 3 + 1.025 ** 2 + 1.025 ** 1)
# # 16 - 20 year
# b = a / 5 * (1.025 ** 5 + 1.025 ** 4 + 1.025 ** 3 + 1.025 ** 2 + 1.025 ** 1)
#
# # print(x)
# print(y)
# print(z)
# print(a)
# print(b)

# print("*" * 20)

# c = 20000 * ((five * five) + (five * three * one) + (five * three) + (five * two) + (five * one) + five + (
#         three * one) + three + two + one)
# print(c)

d = 20000 * ((five * five) + (one * three * five) + (five * three) + (five * two) + (five * one) + five + (
        three * one) + three + two + one)
print(d)
# print(20000 * (five * five))
#
# print(20000 * (one * three * five))
# print(20000 * (five * three * one))
# print((20000 * three) * five)
# print((20000 * five) * three)
# print(20000 * (three * three * three))
# print(20000 * (two * two * two * two * one))
# print(20000 * (one * two * two * two * two))


# d = 228000 * five * five
# print(d)
