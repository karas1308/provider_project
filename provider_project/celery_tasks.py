import django
from celery.schedules import crontab

from email_sender import mail_sender
from logger import log

django.setup()
from celery import Celery

from account.models import User, UserService
from common import get_utc_date_time
from constants import user_confirm_body, user_suspended_notif_body
from service.models import ServiceRate

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "provider_project.settings")

#

celery = Celery('provider_project')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()
celery.conf.timezone = 'Europe/Kiev'


#
def check_balances_and_notify(user):
    user_services = get_user_services(user)
    user_service_names = [service.service.name for service in user_services]
    user_balance = user_services[0].user.balance
    service_rates = ServiceRate.objects.filter(start_date__lte=get_utc_date_time(date_format="%Y-%m-%d"),
                                               end_date__gt=get_utc_date_time(date_format="%Y-%m-%d"),
                                               service__name__in=user_service_names)
    services_price = sum(rate.price for rate in service_rates)
    if services_price / 10 > user_balance >= services_price / 30:
        email_body = user_confirm_body.format(user.balance, int(user_balance / (services_price / 30)))
        # mail_sender(user.email, email_body)
    elif user_balance < services_price / 30:
        email_body = user_suspended_notif_body.format(user.balance)
        # mail_sender(user.email, email_body)
        user_service_to_block = UserService.objects.filter(user=user)
        user_service_to_block.update(is_active=False)


def daily_balance_decrease(user):
    user_services = get_user_services(user)
    user_service_names = [service.service.name for service in user_services]
    user_balance = user_services[0].user.balance
    service_rates = ServiceRate.objects.filter(start_date__lte=get_utc_date_time(date_format="%Y-%m-%d"),
                                               end_date__gt=get_utc_date_time(date_format="%Y-%m-%d"),
                                               service__name__in=user_service_names)

    user_service_to_block = User.objects.filter(id=user.id)
    user_service_to_block.update(balance=user_balance - int(sum(rate.price for rate in service_rates) / 30))


def get_user_services(user):
    return UserService.objects.filter(is_active=True, user=user)


@celery.task
def notif_all_users():
    users = User.objects.filter(is_active=True)
    for user in users:
        log.info("check balance. User id %s".format(user.id))
        check_balances_and_notify(user)


@celery.task
def daily_balance_decrease_all():
    users = User.objects.filter(is_active=True)
    for user in users:
        log.info("decrease balance. User id %s".format(user.id))
        daily_balance_decrease(user)


celery.conf.beat_schedule = {
    'task1': {
        'task': 'provider_project.celery_tasks.daily_balance_decrease_all',
        'schedule': crontab(hour="12", minute="45"),
    },
    'task2': {
        'task': 'provider_project.celery_tasks.notif_all_users',
        'schedule': crontab(hour="12", minute="46"),
    },

}
