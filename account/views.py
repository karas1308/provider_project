from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render

from account.models import User, UserAddress, UserService
from billing.models import Transaction
from config import HOSTNAME
from constants import user_subscribe_service_body
from email_sender import mail_sender
from logger import log
from service.models import Building, City, Region, Service, Street


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
        regions = None
        cities = None
        streets = None
        buildings = None
        region = request.GET.get("region")
        city = request.GET.get("city")
        street = request.GET.get("street")
        building = request.GET.get("building")
        user_address = None
        try:
            user_address = user_info.useraddress
        except Exception:
            pass
        if not user_address:
            regions = Region.objects.all()
            cities = City.objects.filter(region__name=region)
            streets = Street.objects.filter(region__name=region,
                                            city__name=city)
            buildings = Building.objects.filter(region__name=region,
                                                city__name=city,
                                                street__name=street)
        if region and city and street and building:
            apt = request.GET.get("apt")
            entrance = request.GET.get("entrance")
            floor = request.GET.get("floor")
            UserAddress.objects.create(user=request.user,
                                       region=Region.objects.get(name=region),
                                       city=City.objects.get(name=city),
                                       street=Street.objects.get(name=street),
                                       building=Building.objects.get(building=building),
                                       apt=apt,
                                       entrance=entrance,
                                       floor=floor)
        return render(request, template_name="account/index.html",
                      context={"user_info": user_info,
                               "user_address": user_address,
                               "user_services": user_services,
                               "active_transactions": active_transactions,
                               "services_to_subscribe": services_to_subscribe,
                               "regions": regions,
                               "cities": cities,
                               "streets": streets,
                               "buildings": buildings
                               })
    return render(request, template_name="account/index.html")


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
            return redirect(f'http://{HOSTNAME}:8000/account')
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
            return redirect(f'http://{HOSTNAME}:8000/account/login')
        else:
            response_text = "fail"
            return HttpResponseNotFound(response_text)
    return render(request, template_name="account/register.html")


def user_update(request):
    pass


def subscribe_services(request):
    if request.method == "POST":
        services_to_subscribe = request.POST.get("services_to_subscribe")
        services_to_subscribe = Service.objects.get(name=services_to_subscribe)
        UserService.objects.create(user=request.user, service=services_to_subscribe)
        email_body = user_subscribe_service_body.format(services_to_subscribe)
        log.info("Sending notification to user email '%s'".format(request.user.email))
        mail_sender(request.user.email, email_body)
    return redirect(f'http://{HOSTNAME}:8000/account')
