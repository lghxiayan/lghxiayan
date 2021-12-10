#!/usr/bin/conda python
# -*- coding: utf-8 -*-
# @Time : 2021/12/09 17:08
# @Author : xiayan
# @Email : lghxiayan@163.com
import random


class Die:
    """骰子类"""

    def __init__(self, sides=6):
        """初始化"""
        self.sides = sides

    def roll_die(self, num=10):
        for i in range(num):
            dice = random.randint(1, self.sides)
            print(dice, end=',')


my_dice = Die(100)
my_dice.roll_die(30)
