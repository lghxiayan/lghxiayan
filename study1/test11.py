import random


def print_info():
    print('-' * 50)
    print('模拟球员的胜率')
    print('-' * 50)


def get_input():
    try:
        pro_a = eval(input('请输入球员的能力值(0~1之间的小数):'))
        pro_b = eval(input('请输入球员的能力值(0~1之间的小数):'))
        round_num = eval(input('请输入比赛的场数(整数):'))
        return pro_a, pro_b, round_num
    except:
        print('输入的数值有误,程序退出')


def game_start(pro_a, pro_b, round_num):
    sum_a, sum_b = 0, 0
    for i in range(round_num):
        random_pro = random.random()
        if random_pro >= pro_a:
            sum_b += 1
        else:
            sum_a += 1
    return sum_a, sum_b


def print_result(sum_a, sum_b):
    n = sum_a + sum_b
    print('共进行了{}场比赛'.format(n))
    print('球员proA获得{}场比赛,胜率为{:.2f}%'.format(sum_a, sum_a / n * 100))
    print('球员proB获得{}场比赛,胜率为{:.2f}%'.format(sum_b, sum_b / n * 100))


def main():
    print_info()
    pro_a, pro_b, round_num = get_input()
    sum_a, sum_b = game_start(pro_a, pro_b, round_num)
    print_result(sum_a, sum_b)


if __name__ == '__main__':
    main()
