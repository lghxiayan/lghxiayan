import unittest
from unittest.mock import MagicMock, patch
from PySide6.QtWidgets import QApplication, QTextEdit
import logging
import threading

# 假设 WoWJumpController 在模块中定义
from wowjump_controller import WoWJumpController, OutputSignal


class TestWoWJumpController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 创建一个 QApplication 实例
        cls.app = QApplication([])

    @classmethod
    def tearDownClass(cls):
        # 关闭 QApplication 实例
        cls.app.quit()

    def setUp(self):
        self.ui = MagicMock()
        self.ui.textEdit_wowjump_1 = QTextEdit()
        self.controller = WoWJumpController(self.ui)

    @patch('subprocess.Popen')
    def test_on_run_button_clicked(self, mock_popen):
        mock_popen.return_value = MagicMock()
        self.controller.on_run_button_clicked()
        self.assertIn("wowjump 页面里面的 pushButton[run] 被点击了！\n", self.ui.textEdit_wowjump_1.toPlainText())
        self.assertTrue(isinstance(self.controller.process, threading.Thread))

    @patch('subprocess.Popen')
    def test_run_script(self, mock_popen):
        mock_process = MagicMock()
        mock_process.stdout.readline.return_value = "Test output"
        mock_process.poll.return_value = None
        mock_popen.return_value = mock_process

        self.controller.run_script("test_script.py")
        self.assertIn("Test output", self.ui.textEdit_wowjump_1.toPlainText())

    @patch('subprocess.Popen')
    def test_on_stop_button_clicked(self, mock_popen):
        mock_process = MagicMock()
        mock_process.poll.return_value = None
        self.controller.process = mock_process

        self.controller.on_stop_button_clicked()
        self.assertIn("wowjump 页面里面的 pushButton[stop] 被点击了！\n", self.ui.textEdit_wowjump_1.toPlainText())
        mock_process.terminate.assert_called_once()
        mock_process.wait.assert_called_once()

    def test_scroll_to_end(self):
        self.ui.textEdit_wowjump_1.insertPlainText("Some text\n")
        self.controller.scroll_to_end(self.ui.textEdit_wowjump_1)
        cursor = self.ui.textEdit_wowjump_1.textCursor()
        self.assertEqual(cursor.position(), len("Some text\n"))

    @patch('logging.Logger')
    def test_append_output_to_textedit(self, mock_logger):
        self.controller.append_output_to_textedit("<html><body>Test output</body></html>")
        self.assertIn("Test output", self.ui.textEdit_wowjump_1.toPlainText())
        mock_logger.error.assert_not_called()

        # 测试异常处理
        with patch.object(self.ui.textEdit_wowjump_1, 'insertHtml', side_effect=Exception("Test exception")):
            self.controller.append_output_to_textedit("<html><body>Test output</body></html>")
            mock_logger.error.assert_called_once_with("发生异常：Test exception")


if __name__ == '__main__':
    unittest.main()
