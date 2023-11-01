from django.shortcuts import render


# Create your views here.
def billing(request):
    return render(request, template_name="billing/index.html")
