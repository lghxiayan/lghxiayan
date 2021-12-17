from survey import AnonymousSurvey

# 定义一个问题，并创建一个调查
question = 'what language did you first learn to speak?'
my_survey = AnonymousSurvey(question)

# 显示问题并存储答案
my_survey.show_question()
print("Enter 'q' at any time to quit.\n")
while True:
    response = input('Language:')
    if response == 'q':
        break
    if response != '':
        my_survey.store_response(response)

# 显示调查结果
print("\nThank you to everyone who participated in the survey!")
my_survey.show_result()
