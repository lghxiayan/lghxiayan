#!/usr/bin/conda python
# -*- coding: utf-8 -*-
# @Time : 2022/08/01 10:41
# @Author : xiayan
# @Email : lghxiayan@163.com

def int2bin(n, count=24):
    return "".join([str((n >> y) & 1) for y in range(count - 1, -1, -1)])
