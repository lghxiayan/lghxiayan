import math

# 定义每天工作日和休息日的变化率
WORK_DAY_RATE = 0.01
REST_DAY_RATE = 0.01
# 计算每天进步1%的年度复合增长率
EVERY_DAY_UP = math.pow(1.01, 365)
EVERY_DAY_UP_0001 = math.pow(1.001, 365)
EVERY_DAY_UP_00001 = math.pow(1.0001, 365)


def work_day_up_rest_day_down(work_rate, rest_rate):
    """
    根据给定的工作日和休息日进步/退步率，计算一年（365天）后的累积效应。

    参数:
    work_rate -- 工作日的进步率
    rest_rate -- 休息日的退步率

    返回:
    一年后根据工作日和休息日变化率计算的累积效应值。
    """
    # 初始化起始值为1，表示初始能力或进度
    cumulative_effect = 1.0

    # 遍历一年中的每一天
    for day in range(365):
        # 如果是周六或周日，应用休息日的退步率
        if day % 7 in [6, 0]:
            cumulative_effect *= (1 - rest_rate)
        else:
            # 否则，应用工作日的进步率
            cumulative_effect *= (1 + work_rate)

    return cumulative_effect


def print_results(every_day_up, work_rate, cumulative_effect):
    result = []
    result.append('每个工作日进步{:.3f}，周末退步1%，一年的power为：{:.3f}'.format(work_rate, cumulative_effect))
    return '\n'.join(result)


def main():
    result = []
    result.append('人生如逆水行舟，不进则退！\n')
    result.append('每天进步1%, 一年的power为：{:.3f}\n'.format(EVERY_DAY_UP))
    # 当工作日进步和休息日退步的累积效应小于每天进步1%的效应时，增加工作日的进步率
    work_day_rate = WORK_DAY_RATE
    max_iterations = 1000  # 设置最大迭代次数
    iteration_count = 0

    while iteration_count < max_iterations:
        cumulative_effect = work_day_up_rest_day_down(work_day_rate, REST_DAY_RATE)
        if cumulative_effect >= EVERY_DAY_UP:
            break
        result.append(print_results(EVERY_DAY_UP, work_day_rate, cumulative_effect))
        work_day_rate += 0.001
        iteration_count += 1

    if iteration_count == max_iterations:
        result.append("达到最大迭代次数，未能找到满足条件的工作日进步率")

    return '\n'.join(result)


if __name__ == "__main__":
    print(main())
