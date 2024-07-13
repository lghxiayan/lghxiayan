import schedule
import time


def job():
    print("I'm working...")


schedule.every(5).seconds.do(job)

job_id = schedule.every().hours.do(job)
print(job_id)

schedule.cancel_job(job_id)

while True:
    schedule.run_pending()
    time.sleep(1)
