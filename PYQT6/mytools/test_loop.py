import time
import logging
from datetime import datetime

# 日志配置
logger = logging.getLogger('loop_controller')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class LoopController:
    """
    LoopController 类用于管理循环执行，支持指定迭代次数、间隔时间和时间单位。

    属性:
    - loop_counter: 循环的最大迭代次数。
    - loop_interval: 循环迭代之间的间隔时间。
    - loop_unit: 循环间隔时间的时间单位（秒、分钟、小时、天）。
    - running: 标志位，指示循环是否正在运行。
    - start_time: 循环开始的时间，默认为当前时间。
    """

    def __init__(self, loop_counter=3, loop_interval=1, loop_unit='second', start_time=None, end_time=None):
        """
        初始化 LoopController 实例，默认或指定参数。

        参数:
        - loop_counter: 循环的最大迭代次数，默认为 3。
        - loop_interval: 循环迭代之间的间隔时间，默认为 1。
        - loop_unit: 循环间隔时间的时间单位，默认为 'second'。

        异常:
        - ValueError: 如果提供了不受支持的时间单位。
        """
        self.counter = 0
        self.loop_counter = loop_counter
        self.loop_interval = loop_interval
        self.is_loop = True
        self.time_units = {'second': 1, 'minute': 60, 'hour': 3600, 'day': 86400}

        if loop_unit not in self.time_units:
            raise ValueError(f'不支持的时间单位: {loop_unit}')
        self.loop_unit = loop_unit
        self.sleep_time = self.loop_interval * self.time_units[self.loop_unit]

        self.start_time = start_time if start_time else datetime.now()
        self.logger = logger

    def run(self):
        """
        使用指定参数执行循环。达到设定的迭代次数后自动停止。

        处理异常:
        - KeyboardInterrupt: 记录用户中断错误。
        - Exception: 记录未知错误。
        """
        try:
            while self.is_loop:
                current_time = datetime.now().replace(microsecond=0)
                elapsed_time = current_time - self.start_time.replace(microsecond=0)
                self.logger.info(f"循环开始，当前时间: {current_time}, 已经运行时间: {elapsed_time}")
                self.counter += 1
                time.sleep(self.sleep_time)

                if self.counter >= self.loop_counter:
                    self.is_loop = False
        except KeyboardInterrupt:
            self.logger.error("用户中断循环")
        except SystemExit:
            self.logger.error('系统退出')
        except Exception as e:
            self.logger.error(f"发生未知错误: {e}")

    def stop(self):
        """
        停止循环执行。
        """
        self.is_loop = False
        self.logger.info("循环已停止")


if __name__ == '__main__':
    controller = LoopController()
    controller.run()
