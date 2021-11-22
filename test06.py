import turtle
import time


def drawGap(num):
    turtle.penup()
    turtle.fd(num)


def drawLine(draw):
    # turtle.delay(100)
    drawGap(5)
    turtle.pendown() if draw else turtle.penup()
    turtle.fd(30)
    drawGap(5)
    turtle.right(90)


def drawAdd(draw):
    drawGap(20)
    turtle.right(90)
    drawGap(25)
    turtle.pendown() if draw else turtle.penup()
    drawGap(-60)
    turtle.left(90)
    drawGap(-20)


def drawDigit(digit):
    drawLine(True) if digit in [2, 3, 4, 5, 6, 8, 9, '-', '=', '+'] else drawLine(False)
    drawLine(True) if digit in [0, 1, 3, 4, 5, 6, 7, 8, 9] else drawLine(False)
    drawLine(True) if digit in [0, 2, 3, 5, 6, 8, 9, '='] else drawLine(False)
    drawLine(True) if digit in [0, 2, 6, 8, ] else drawLine(False)
    turtle.left(90)
    drawLine(True) if digit in [0, 4, 5, 6, 8, 9] else drawLine(False)
    # drawAdd(True) if digit in ['+'] else print('pass this line')
    drawLine(True) if digit in [0, 2, 3, 5, 6, 7, 8, 9] else drawLine(False)
    drawLine(True) if digit in [0, 1, 2, 3, 4, 7, 8, 9] else drawLine(False)
    turtle.left(180)
    turtle.penup()
    turtle.fd(20)


def drawDate(date):
    if date:
        for i in date:
            if i.isdigit():
                drawDigit(eval(i))
            elif i == '-':
                turtle.write('年', font=('Arial', 18, 'normal'))
                turtle.pencolor('red')
                turtle.fd(40)
            elif i == '=':
                turtle.write('月', font=('Arial', 18, 'normal'))
                turtle.pencolor('blue')
                turtle.fd(40)
            elif i == '+':
                turtle.write('日', font=('Arial', 18, 'normal'))
                turtle.pencolor('pink')
                turtle.fd(40)
            else:
                pass

    if date == None:
        # date = time.strftime("%Y-%m=%d+", time.gmtime())
        print('hello')


def main():
    turtle.setup(800, 600, 200, 200)
    turtle.width(5)
    turtle.pencolor('green')
    turtle.penup()
    turtle.fd(-300)
    # drawDate()
    # drawDate('2018-30=50+')
    drawDate(time.strftime("%Y-%m=%d+", time.gmtime()))
    turtle.hideturtle()
    turtle.done()


if __name__ == '__main__':
    main()
