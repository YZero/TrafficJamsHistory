import datetime

from celery.task import task


@task()
def task_number_two():
    print(datetime.datetime.now())
