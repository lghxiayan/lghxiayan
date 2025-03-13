import os

# 确保 Python 解释器和终端使用的默认编码为 UTF-8，因为windows默认使用是GBK
os.environ['PYTHONIOENCODING'] = 'utf-8'


class App:
    @staticmethod
    def setup_logging():
        log_file_name = "app.txt"
        return log_file_name


class CCC:
    def __init__(self, new_name):
        self.new_name = new_name
        print(self.new_name)


if __name__ == "__main__":
    app = App()
    a_name = app.setup_logging()
    print(a_name)

    CCC(a_name)
