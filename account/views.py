from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render

from account.models import User


# Create your views here.
def account(request):
    return render(request, template_name="account/index.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            response_text = "ok"
            return HttpResponse(response_text)
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
