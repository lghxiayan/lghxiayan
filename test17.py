#!/usr/bin/conda python
# -*- coding: utf-8 -*-
# @Time : 2021/11/30 9:20
# @Author : xiayan
# @Email : lghxiayan@163.com

def func():
    fs = []
    for i in range(3):
        print('进入lam前i的值：', i)

        def lam(x):
            print('进入lam后i的值：', i)
            return x * i

        fs.append(lam)
    return fs


F = func()
print(F)

for f in F:
    print(f(20))
