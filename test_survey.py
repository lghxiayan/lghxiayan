import unittest

from survey import AnonymousSurvey


class TestAnonymousSurvey(unittest.TestCase):
    """创建测试类"""

    def test_store_single_response(self):
        """测试单个答案存储"""
        question = '你的问题是:'
        my_survey = AnonymousSurvey(question)
        my_survey.store_response('English')
        self.assertIn('English', my_survey.responses)

    def test_store_three_response(self):
        """测试三个答案的存储"""
        question = '你的问题是：'
        my_survey = AnonymousSurvey(question)
        responses = ['English', 'Chinese', 'Spanish']
        for response in responses:
            my_survey.store_response(response)

        for response in responses:
            self.assertIn(response, my_survey.responses)


if __name__ == '__main__':
    unittest.main()
