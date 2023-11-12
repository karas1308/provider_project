from django.urls import path

from . import views

urlpatterns = [
    path('', views.account, name="account"),
    path('logout/', views.user_logout, name="user_logout"),
    path('login/', views.user_login, name="user_login"),
    path('register/', views.user_register, name="user_register"),
    path('subscribe_services/', views.subscribe_services, name="subscribe_services"),
    # path('check_balances_and_notify/', views.check_balances_and_notify, name="check_balances_and_notify"),

]
