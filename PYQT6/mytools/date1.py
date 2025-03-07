import datetime

now = datetime.datetime.now().replace(microsecond=0)
print(now)
print(now.date())
print(now.time())
