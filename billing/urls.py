from django.urls import path

from . import views

urlpatterns = [

    path('', views.billing, name="billing"),
    path('pay/', views.pay, name="pay"),
]
