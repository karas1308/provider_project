import os
from datetime import timedelta

from celery import Celery

from account.models import User, UserService
from common import get_utc_date_time
from service.models import ServiceRate
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "provider_project.settings")
app = Celery('celery_task', broker='pyamqp://guest@rabbit_mq//')
# app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task
def check_balances_and_notify(user_id):
    users = User.objects.filter(is_active=True)
    user_service = UserService.objects.get(is_active=True)
    service_rates = ServiceRate.objects.get(start_date__lte=get_utc_date_time(date_format="%Y-%m-%d"),
                                            end_date__gt=get_utc_date_time(date_format="%Y-%m-%d"))
    tasks = []
    # for user in users:
    # email_body = user_confirm_body.format(user.balance)
    # mail_sender(user.email, email_body)


app.conf.beat_schedule = {
    'task1': {
        'task': 'celery_task.task1',
        'schedule': timedelta(seconds=5)
    },
    'task2': {
        'task': 'celery_task.task2',
        'schedule': timedelta(seconds=10)
    }
}


@app.task
def notif_all_users():
    users = User.objects.filter(is_active=True)
    for user in users:
        check_balances_and_notify.delay(user)


@app.task(queue='worker1')
def task_1():
    print("task_1")


@app.task(queue='beat1')
def task_2():
    print("task_2")


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(10.0, check_balances_and_notify.s('hello'), name='add every 10')

    # Calls test('hello') every 30 seconds.
    # It uses the same signature of previous task, an explicit name is
    # defined to avoid this task replacing the previous one defined.
    # for n in users:
    # sender.add_periodic_task(30.0, notif_all_users.s(), name='add every 30')

    # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )
    # result1 = task_1.delay()
    # result2 = task_2.delay()
