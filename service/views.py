from django.shortcuts import render

from provider_project.celery_tasks import notif_all_users
from service.models import Service


# Create your views here.
def index(request):
    services = Service.objects.all()
    return render(request, template_name="services/index.html", context={"services": services})


def notify():
    notif_all_users.delay()
