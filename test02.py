workDay = 0.01
restDay = 0.01
everyDayUp = pow(1.01, 365)


def workDayUp_restDayDown(workDay, restDay):
    day = 1
    for i in range(365):
        if i % 7 in [6, 0]:
            day = day * (1 - restDay)
        else:
            day = day * (1 + workDay)
    print('每天进步1%,power为：', everyDayUp)
    print('每个工作日进步{:.3f}，周未退步1%，power为：'.format(workDay), day)
    return day


while workDayUp_restDayDown(workDay, 0.01) < everyDayUp:
    workDay += 0.001
