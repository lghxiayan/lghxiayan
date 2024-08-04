from pywebio.input import input, FLOAT, input_group, TEXT
from pywebio.output import put_text, put_scope, use_scope, clear, put_button, put_html
from pywebio import start_server


def calculate_bmi():
    # 创建输入框
    inputs = input_group('BMI计算', [
        input('请输入你的身高(cm):', name='height', type=FLOAT, value=170,
              placeholder='中华人民共和国中华人民共和国中华人民共和国中华人民共和国中华人民共和国中华人民共和国'),
        input('请输入你的体重(kg):', name='weight', type=FLOAT, value=60),
    ])
    height = inputs['height']
    weight = inputs['weight']

    # 创建按钮
    put_button('计算BMI', onclick=lambda: submit_bmi(height, weight))

    # 创建一个作用域用于存放结果
    put_scope('bmi_result')


def submit_bmi(height, weight):
    bmi = weight / (height / 100) ** 2

    top_status = [(14.9, '极瘦'), (18.4, '偏瘦'), (22.9, '正常'),
                  (27.5, '过重'), (40.0, '肥胖'), (float('inf'), '非常肥胖')]

    # 进入作用域并清除之前的内容
    with use_scope('bmi_result'):
        for top, status in top_status:
            if bmi <= top:
                put_text('你的 BMI 值: %.1f, 身体状态: %s' % (bmi, status))
                break


if __name__ == '__main__':
    start_server(calculate_bmi, debug=True, port=8001)
