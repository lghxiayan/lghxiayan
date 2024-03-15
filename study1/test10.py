try:
    user_input = input()
    if complex(user_input) == complex(eval(user_input)):
        output = pow(eval(user_input), 2)
        print(output)

except:
    print('输入有误')
