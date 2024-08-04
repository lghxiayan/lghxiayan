from pywebio.input import input_group, input, TEXT, PASSWORD, NUMBER, RADIO, CHECKBOX, checkbox, radio, TEXTAREA, \
    textarea
from pywebio.output import put_text, put_markdown
from pywebio import start_server
import config_ptvicomo_04 as config


def read_config_from_file():
    # 直接从配置文件中读取参数

    return {
        'CHROME_DRIVER_PATH': config.CHROME_DRIVER_PATH,
        'DB_CONFIG': config.DB_CONFIG,
        'TABLE_NAME': config.TABLE_NAME,
        'WEBSITE_URL': config.WEBSITE_URL,
        'WAIT_TIMEOUT': config.WAIT_TIMEOUT,
        'CURRENT_ACTION': config.CURRENT_ACTION,
        'SALE_NUMBER': config.SALE_NUMBER,
        'BUY_NUMBER': config.BUY_NUMBER,
        'PROFIT_MARGIN': config.PROFIT_MARGIN,
        'SAVE_PAGE': config.SAVE_PAGE
    }


def read_config_from_web():
    config_dict = read_config_from_file()

    # CURRENT_ACTION = {'buy': '买入', 'sale': '卖出', 'get_data': '提取数据'}

    # 使用配置文件中的值作为表单的默认值
    config = input_group("象岛_数据采集配置", [
        input(label='ChromeDriver路径', name='chrome_driver_path', type=TEXT, value=config_dict['CHROME_DRIVER_PATH'],
              placeholder='请输入ChromeDriver路径', readonly=True),
        input(label='数据库主机地址', name='db_host', type=TEXT, value=config_dict['DB_CONFIG']['host'],
              placeholder='请输入数据库主机地址'),
        input(label='数据库端口', name='db_port', type=NUMBER, value=config_dict['DB_CONFIG']['port'],
              placeholder='请输入数据库端口'),
        input(label='数据库用户名', name='db_user', type=TEXT, value=config_dict['DB_CONFIG']['user'],
              placeholder='请输入数据库用户名'),
        input(label='数据库密码', name='db_password', type=PASSWORD, value=config_dict['DB_CONFIG']['password'],
              placeholder='请输入数据库密码'),
        input(label='数据库名称', name='db_name', type=TEXT, value=config_dict['DB_CONFIG']['database'],
              placeholder='请输入数据库名称'),
        input(label='表名称', name='table_name', type=TEXT, value=config_dict['TABLE_NAME'],
              placeholder='请输入表名称'),
        input(label='网站URL', name='website_url', type=TEXT, value=config_dict['WEBSITE_URL'],
              placeholder='请输入网站URL'),
        input(label='等待超时时间', name='wait_timeout', type=NUMBER, value=config_dict['WAIT_TIMEOUT'],
              placeholder='请输入等待超时时间'),
        input(label='卖出数量', name='sale_number', type=NUMBER, value=config_dict['SALE_NUMBER'],
              placeholder='请输入卖出数量'),
        input(label='买入数量', name='buy_number', type=NUMBER, value=config_dict['BUY_NUMBER'],
              placeholder='请输入买入数量'),
        input(label='利润率', name='profit_margin', type=NUMBER, value=config_dict['PROFIT_MARGIN'],
              placeholder='请输入利润率'),
        radio('是否保存页面', name='save_page', value=config_dict['SAVE_PAGE'],
              options=[{'label': '是', 'value': True}, {'label': '否', 'value': False}], ),
        textarea(label='备注', name='remark', placeholder='请输入备注', value='测试测试'),
    ])

    # 输出确认信息
    put_text("配置已收集，以下是您输入的参数：")
    put_markdown(f"""
    - ChromeDriver路径: {config['chrome_driver_path']}
    - 数据库主机地址: {config['db_host']}
    - 数据库端口: {config['db_port']}
    - 数据库用户名: {config['db_user']}
    - 数据库名称: {config['db_name']}
    - 表名称: {config['table_name']}
    - 网站URL: {config['website_url']}
    - 等待超时时间: {config['wait_timeout']}
    - 卖出数量: {config['sale_number']}
    - 买入数量: {config['buy_number']}
    - 利润率: {config['profit_margin']}
    - 是否保存页面: {config['save_page']}
    - 备注: {config['remark']}
    """)

    return config


def main():
    config = read_config_from_web()
    # 使用config字典中的值来更新你的配置文件或直接使用它们


if __name__ == '__main__':
    main()
