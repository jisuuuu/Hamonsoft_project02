from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
import time
from .hamon_language import run
from functools import partial


class Scheduler(object):
    def __init__(self):
        self.sched = BackgroundScheduler()
        self.sched.start()
        self.job_id = ""

    def __del__(self):
        self.shutdown()

    def shutdown(self):
        self.sched.shutdown()

    def kill_scheduler(self, job_id):
        try:
            print('%s Scheduler End' % job_id)
            self.sched.remove_job(job_id)
        except JobLookupError as err:
            print('fail to stop scheduler: %s' % err)
            return

    def hello(self, job_id):
        print('%s scheduler process_id[%s] : %d' %( job_id, time.localtime().tm_sec ))

    def scheduler(self, job_id, read, period, idx):
        print('%s Scheduler Start' % job_id)

        period_list = period.split()

        func1 = partial(run, read)
        func = partial(func1, idx)
        self.sched.add_job(func, 'cron', minute=period_list[0], hour=period_list[1], day=period_list[2], month=period_list[3], year=period_list[4], id=job_id)