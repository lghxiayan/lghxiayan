#!/usr/bin/conda python
# -*- coding: utf-8 -*-
# @Time : 2021/11/24 8:40
# @Author : xiayan
# @Email : lghxiayan@163.com


import tabulate

data = [["北京理工大学", "985", 2000], \
        ["清华大学", "985", 3000], \
        ["大连理工大学", "985", 4000], \
        ["深圳大学", "211", 2000], \
        ["沈阳大学", "省本", 2000], \
        ]

print(tabulate.tabulate(data, tablefmt='grid'))
