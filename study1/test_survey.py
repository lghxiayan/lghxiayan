import unittest

from survey import AnonymousSurvey


class TestAnonymousSurvey(unittest.TestCase):
    """创建测试类"""

    def setUp(self):
        """创建共用对象"""
        question = '你的问题是:'
        self.my_survey = AnonymousSurvey(question)
        self.responses = ['English', 'Chinese', 'Spanish']

    def test_store_single_response(self):
        """测试单个答案存储"""
        self.my_survey.store_response(self.responses[0])
        self.assertIn(self.responses[0], self.my_survey.responses)

    def test_store_three_response(self):
        """测试三个答案的存储"""
        for response in self.responses:
            self.my_survey.store_response(response)

        for response in self.responses:
            self.assertIn(response, self.my_survey.responses)


if __name__ == '__main__':
    unittest.main()
