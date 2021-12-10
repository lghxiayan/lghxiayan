#!/usr/bin/conda python
# -*- coding: utf-8 -*-
# @Time : 2021/12/09 17:17
# @Author : xiayan
# @Email : lghxiayan@163.com

import random


class Caipiao:
    """彩票类"""

    def __init__(self, list1=('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                              'j', 'k', 'l', 'm', 'n', 1, 2, 3, 4, 5)):
        self.list1 = list1
        self.output = ''

    def get_four(self):
        """取4个字母或数字"""
        list2 = random.choices(self.list1, k=4)
        self.output = ''.join([str(i) for i in list2])
        print(f"中奖号码是：{self.output}")

    def get_my_ticket(self):
        active = True
        my_sum = 0
        while active:
            cp = random.choices(self.list1, k=4)
            my_ticket = ''.join([str(i) for i in cp])
            if my_ticket == self.output:
                print(f"恭喜你中奖了！中奖号码是{my_ticket} 一共尝试了{my_sum}次.")
                active = False
            my_sum += 1


cp1 = Caipiao()
cp1.get_four()
cp1.get_my_ticket()
