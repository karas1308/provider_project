from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render

from account.models import User, UserService
from billing.models import Transaction
from common import get_utc_date_time
from config import HOSTNAME
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


def check_balances_and_notify(request):
    user_service = UserService.objects.filter(is_active=True, user__is_active=True)
    service_rates = ServiceRate.objects.filter(start_date__lte=get_utc_date_time(date_format="%Y-%m-%d"),
                                               end_date__gt=get_utc_date_time(date_format="%Y-%m-%d"))
    print(user_service)


def subscribe_services(request):
    services_to_subscribe = request.POST.get("services_to_subscribe")
    services_to_subscribe = Service.objects.get(name=services_to_subscribe)
    UserService.objects.create(user=request.user, service=services_to_subscribe)
    return redirect(f'http://{HOSTNAME}:8000/account')
