import pandas as pd

col_names = ['户名', '1月份合计用电量（万kWh）', '2月份合计用电量（万kWh）', '3月份合计用电量（万kWh）',
             '4月份合计用电量（万kWh）', '5月份合计用电量（万kWh）', '6月份合计用电量（万kWh）']

reorder_col_names = ['户名', '2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06']

replace_col_names = {'1月份合计用电量（万kWh）': '2024-01', '2月份合计用电量（万kWh）': '2024-02',
                     '3月份合计用电量（万kWh）': '2024-03', '4月份合计用电量（万kWh）': '2024-04',
                     '5月份合计用电量（万kWh）': '2024-05', '6月份合计用电量（万kWh）': '2024-06'}


def open_csv(file_, col_names_):
    df_ = pd.read_excel(file_, usecols=col_names_)
    return df_


def row_to_col(df_):
    # 确保'户名'列被正确设置为id_vars
    melted_df = df_.melt(id_vars='户名', var_name='月份', value_name='用电量')
    print('行列互换成功')
    return melted_df


def df_to_excel(df_, file_):
    df_.to_excel(file_, index=False)
    print('数据导出完成！')
    return None


def df_rename(df_, col_names_):
    df_.rename(columns=col_names_, inplace=True)
    print('列名替换成功！')
    return df_


if __name__ == '__main__':
    df = open_csv('dl_2024.xlsx', col_names)
    # print(df)
    # df.columns = renew_col_names
    # print(df.columns)
    print(df.sample(3))

    df = df_rename(df, replace_col_names)
    print(df.sample(3))

    df = df.reindex(columns=reorder_col_names)
    print(df.sample(3))
    
    df_to_excel(df, 'dl_2024_new.xlsx')
