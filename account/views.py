import decimal

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render

from account.models import User, UserService
from billing.models import Transaction
from common import get_utc_date_time
from config import HOSTNAME
from constants import user_confirm_body, user_suspended_notif_body
from provider_project.celery_tasks import get_user_services
from service.models import Service, ServiceRate


# Create your views here.
def account(request):
    if request.user.is_authenticated:
        user_info = User.objects.get(id=request.user.id)
        active_transactions = Transaction.objects.filter(user=user_info, is_expired=False).all()
        services = Service.objects.all()
        user_services = UserService.objects.filter(user=user_info, is_active=True)
        user_services_names = [user_service.service.name for user_service in user_services]
        services_to_subscribe = []
        if user_services:
            for service in services:
                if service.name not in user_services_names:
                    services_to_subscribe.append(service)
        else:
            services_to_subscribe = services
        return render(request, template_name="account/index.html",
                      context={"user_info": user_info, "user_services": user_services,
                               "active_transactions": active_transactions,
                               "services_to_subscribe": services_to_subscribe})
    return render(request, template_name="account/login.html")


def user_login(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        user = authenticate(
            request,
            phone=phone,
            password=password
        )
        if user is not None:
            login(request, user, backend="account.utils.PhoneBackend")
            # response_text = "ok"
            user_info = User.objects.get(phone=phone)
            return render(request, template_name="account/index.html", context={"user_info": user_info})
            # return HttpResponse(response_text)
        else:
            response_text = "fail"
            return HttpResponseNotFound(response_text)
    if request.user.is_authenticated:
        return redirect("/")
    return render(request, template_name="account/login.html")


def user_logout(request):
    logout(request)
    return redirect("/")


def user_register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")
        telegram = request.POST.get("telegram")
        password = request.POST.get("password")
        user = User.objects.create(first_name=first_name,
                                   last_name=last_name,
                                   phone=phone,
                                   email=email,
                                   telegram=telegram,
                                   password=password,
                                   )
        if user.phone == phone:
            return JsonResponse({"username": user.phone}, safe=False)
        else:
            response_text = "fail"
            return HttpResponseNotFound(response_text)
    return render(request, template_name="account/register.html")

#
# def check_balances_and_notify(request):
#     user_services = get_user_services(request.user)
#     user_service_names = [service.service.name for service in user_services]
#     user_balance = user_services[0].user.balance
#     service_rates = ServiceRate.objects.filter(start_date__lte=get_utc_date_time(date_format="%Y-%m-%d"),
#                                                end_date__gt=get_utc_date_time(date_format="%Y-%m-%d"),
#                                                service__name__in=user_service_names)
#     services_price = sum(rate.price for rate in service_rates)
#     if services_price / 10 > user_balance >= services_price / 30:
#         email_body = user_confirm_body.format(request.user.balance,
#                                               int(user_balance / decimal.Decimal((services_price / 30))))
#         # mail_sender(user.email, email_body)
#     elif user_balance < services_price / 30:
#         email_body = user_suspended_notif_body.format(request.user.balance)
#         # mail_sender(user.email, email_body)
#         user_service_to_block = UserService.objects.filter(user=request.user)
#         user_service_to_block.update(is_active=False)
#

def subscribe_services(request):
    services_to_subscribe = request.POST.get("services_to_subscribe")
    services_to_subscribe = Service.objects.get(name=services_to_subscribe)
    UserService.objects.create(user=request.user, service=services_to_subscribe)
    return redirect(f'http://{HOSTNAME}:8000/account')
