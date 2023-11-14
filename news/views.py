from django.shortcuts import render

from common import get_utc_date_time
from news.models import News


# Create your views here.
def news(request):
    active_news = News.objects.filter(
        create_at__gt=get_utc_date_time(amount_of_days=-7, date_format="%Y-%m-%d")).order_by('-create_at')
    return render(request, template_name="news/index.html", context={"news": active_news})
