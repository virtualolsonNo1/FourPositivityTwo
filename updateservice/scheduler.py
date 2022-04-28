from apscheduler.schedulers.background import BackgroundScheduler
from updateservice import update
def start():
    scheduler=BackgroundScheduler()
    # run both jobs every minute
    scheduler.add_job(update.updateDailyPoints,'interval',minutes=1)
    scheduler.add_job(update.notifyUsers, 'interval', minutes=1)
    print("Starting scheduler")
    # start all jobs
    scheduler.start()