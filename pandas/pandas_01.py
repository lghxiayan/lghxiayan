import pandas as pd

data = {
    'student_id': [1, 2, 3],
    'name': ['张三', '李四', '王五'],
    'math': [80, 90, 70],
    'english': [90, 80, 70],
    'science': [85, 95, 85]
}

df = pd.DataFrame(data)
print(df)
print('--' * 50)

melted_df = df.melt(id_vars=['name', 'student_id'], var_name='科目', value_name='成绩')
print(melted_df)
