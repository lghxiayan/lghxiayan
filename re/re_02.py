import re

sale_turnip_text = """
象岛农庄 【鲜红象胡萝卜条 - 作物成熟 - 开售中】
农作物已成熟，保质期至下周六晚24:00
鲜红象胡萝卜条的价格是523.0，保质期至下周六晚24:00，要马上进货吗？

输入进货数量(剩余配货量为0kg 提升等级以获得更高配货量)
"""

pattern = "[\u4e00-\u9fff]+(?=的价格是)"
result = re.search(pattern, sale_turnip_text).group()
# result = int(result)
print(type(result), result)
