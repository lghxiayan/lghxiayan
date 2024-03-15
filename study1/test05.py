import turtle as t
from netAssist import time
import yaml

BAIFEN = pow(1.01, 365)
QIANFEN = pow(1.001, 365)


def get_canshu():
    try:
        with open('mypro_config.yaml') as f:
            data = yaml.load(f, yaml.FullLoader)
        f.close()
    except:
        print('打开文件出错')
    return data


def turtle(start_date):
    t.setup(800, 600, 200, 200)
    t.title('慎独，变强！')
    t.penup()
    t.pencolor('blue')
    t.pensize(5)
    t.goto(-350, 200)
    # t.fd(-350)
    t.write("每天努力百分之一,一年后会变强{:.2f}倍".format(BAIFEN), font=("微软雅黑", 30, 'normal'))
    t.goto(-350, 150)
    t.write("每天努力千分之一,一年后会变强{:.2f}倍".format(QIANFEN), font=("微软雅黑", 30, 'normal'))
    t.goto(-350, 100)
    t.write("开始时间为：{}".format(start_date), font=("微软雅黑", 30, 'normal'))

    t.goto(-350, 50)
    for i in range(10):
        NOW_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        t.write("当前时间为：{}".format(NOW_TIME), font=("微软雅黑", 30, 'normal'))
        time.sleep(1)

    t.goto(-350, 0)
    t.write("从开始到现在，一共坚持了XX天", font=("微软雅黑", 30, 'normal'))

    t.goto(-350, -50)
    t.write("每天努力千分之一,到现在已经变强了xxx倍", font=("微软雅黑", 30, 'normal'))


if __name__ == '__main__':
    data = get_canshu()
    start_date = data['start_date']
    turtle(start_date)

    t.hideturtle()
    t.done()
