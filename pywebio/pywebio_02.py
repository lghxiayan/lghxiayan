from pywebio.input import input, FLOAT, input_group
from pywebio.output import put_text, put_html
from pywebio import start_server
from pyecharts.charts import Bar
from PIL import Image


def draw_chart(inputs):
    bar = Bar()
    bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫"])
    bar.add_yaxis("商家A", inputs)
    # render 会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件
    # 也可以传入路径参数，如 bar.render("mycharts.html")
    return bar.render_notebook()


def calculate_bmi():
    inputs = input_group(
        label='输入你的身高和体重',
        inputs=[
            input('请输入你的身高(cm):', type=FLOAT, name='a'),
            input('请输入你的体香(kg):', type=FLOAT, name='b'),
            input('请输入你的体香(kg):', type=FLOAT, name='c'),
        ]
    )

    a = inputs['a']
    b = inputs['b']
    c = inputs['c']

    # bmi = weight / (height / 100) ** 2
    #
    # top_status = [(14.9, '极瘦'), (18.4, '偏瘦'), (22.9, '正常'),
    #               (27.5, '过重'), (40.0, '肥胖'), (float('inf'), '非常肥胖')]
    #
    # for top, status in top_status:
    #     if bmi <= top:
    #         put_text('你的 BMI 值: %.1f,身体状态: %s' % (bmi, status))
    #         break

    put_html(draw_chart([a, b, c]))


if __name__ == '__main__':
    start_server(calculate_bmi, debug=True, port=8001)
    # start_server(calculate_bmi, debug=True, port=8001)
