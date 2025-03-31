import configparser
import configupdater
import os
import logging
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_cookies_save_to_file(self):
    """
    打印当前浏览器会话的所有Cookies
    """
    try:
        cookies = self.driver.get_cookies()
        logger.info(cookies)

        with open('config_ptvicomo_04.py', 'r', encoding='utf-8') as file:
            content = file.read()

        cookie_var_name = 'WEB_COOKIE'
        pattern = re.compile(fr"(?<={cookie_var_name} = )([^]]+)(?=])")
        math = re.findall(pattern, content)
        old_cookies = f"{cookie_var_name} = {math[0]}]"
        # print(f"正则匹配的结果是：{old_cookies}")
        new_cookies = f"{cookie_var_name} = {cookies}"

        if cookie_var_name in content:
            logger.info(f"{cookie_var_name}变量已存在，进行替换操作")
            content = content.replace(old_cookies, new_cookies)
        else:
            logger.info(f"{cookie_var_name}变量不存在，进行添加操作")
            content += f"\n{cookie_var_name} = {cookies}"

        with open('config_ptvicomo_04.py', 'w', encoding='utf-8') as file:
            file.write(content)
            logger.info("config_ptvicomo_04.py文件已更新")
    except Exception as e:
        logger.error(f"NoSuchElementException: {e}")


import configupdater
import os


def save_settings():
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config_ptvicomo_04.ini')

    try:
        # 创建 ConfigUpdater 对象
        updater = configupdater.ConfigUpdater()

        # 读取现有的配置文件
        if os.path.exists(config_file_path):
            updater.read(config_file_path, encoding='utf-8')
        else:
            print("错误", f"配置文件不存在: {config_file_path}")
            return

        # 更新 HEAD_LESS 参数
        if 'DEFAULT' not in updater:
            updater.add_section('DEFAULT')
        updater['DEFAULT']['HEAD_LESS'] = str(True)
        print(f"更新 HEAD_LESS 参数: {updater['DEFAULT']['HEAD_LESS']}")

        # 写入更新后的配置文件
        with open(config_file_path, 'w', encoding='utf-8') as configfile:
            updater.write(configfile)

        print("成功", "设置已保存")
    except Exception as e:
        print("错误", f"保存配置文件时发生异常: {e}")


def save_settings_config_parser():
    config = configparser.ConfigParser(interpolation=None)
    config.optionxform = str  # 保留原始键名
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config_ptvicomo_04.ini')

    try:
        # 读取现有的配置文件
        if os.path.exists(config_file_path):
            with open(config_file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        else:
            print("错误", f"配置文件不存在: {config_file_path}")
            return

        # 读取配置文件内容
        config.read(config_file_path, encoding='utf-8')

        # 更新 HEAD_LESS 参数
        if 'DEFAULT' not in config:
            config['DEFAULT'] = {}
        config['DEFAULT']['HEAD_LESS'] = str(True)
        print(f"更新 HEAD_LESS 参数: {config['DEFAULT']['HEAD_LESS']}")

        # 重新写入整个配置文件，保留注释和 section
        with open(config_file_path, 'w', encoding='utf-8') as configfile:
            current_section = None

            # 写入注释和 section
            for line in lines:
                line = line.strip()
                if line.startswith('[') and line.endswith(']'):  # 处理 section
                    current_section = line[1:-1]
                    configfile.write(f"[{current_section}]\n")
                elif line.startswith('#'):  # 写入注释
                    configfile.write(f"{line}\n")

            # 写入所有键值对
            for section in config.sections() + ['DEFAULT']:
                if section != current_section:  # 避免重复写入 section
                    configfile.write(f"[{section}]\n")
                for key, value in config.items(section):
                    configfile.write(f"{key} = {value}\n")

        print("成功", "设置已保存")
    except Exception as e:
        print("错误", f"保存配置文件时发生异常: {e}")


if __name__ == '__main__':
    save_settings()
