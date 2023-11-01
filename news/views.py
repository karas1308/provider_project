from django.shortcuts import render


# Create your views here.
def news(request):
    return render(request, template_name="news/index.html")
