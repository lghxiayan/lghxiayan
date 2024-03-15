from pywebio.input import *
from pywebio.output import *

slider = slider('滑块输入', value=5, min_value=1, max_value=100, step=1)
put_text(slider)
