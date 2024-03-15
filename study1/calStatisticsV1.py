def getNum():
    nums = []
    iNumStr = input('请输入数字(按回车退出):')
    while iNumStr != '':
        nums.append(eval(iNumStr))
        iNumStr = input('请输入数字(按回车退出):')
    return nums


def mean(numbers):
    s = 0.0
    for num in numbers:
        s += num
    return s / len(numbers)


def dev(numbers, mean):
    sdev = 0.0
    for num in numbers:
        sdev += (num - mean) ** 2
    return pow(sdev / (len(numbers) - 1), 0.5)


def median(numbers):
    numbers = sorted(numbers)
    size = len(numbers)
    if size % 2 == 0:
        med = (numbers[size // 2 - 1] + numbers[size // 2]) / 2
    else:
        med = numbers[size // 2]
    return med


s1 = getNum()
s2 = mean(s1)

print('平均值:{},方差:{:.1f},中位数:{}'.format(s2, dev(s1, s2), median(s1)))
