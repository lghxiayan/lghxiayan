class AnonymousSurvey:
    """收集匿名调查问卷的答案"""

    def __init__(self, question):
        """初始化"""
        self.question = question
        self.responses = []

    def show_question(self):
        """显示调查问卷"""
        print(self.question)

    def store_response(self, response):
        """存储单份调查答案"""
        self.responses.append(response)

    def show_result(self):
        """显示收集到的所有答案"""
        print("Survey result:")
        for response in self.responses:
            print(f"- {response}")
