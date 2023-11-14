from django.shortcuts import redirect, render
from liqpay import LiqPay

from billing.common import update_transactions_statuses
from billing.models import Transaction
from common import get_utc_date_time, order_id
from config import HOSTNAME, LIQPAY_PRIVATE_KEY, LIQPAY_PUBLIC_KEY
from service.models import Service


# Create your views here.
def billing(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
        services = Service.objects.all()
        return render(request, template_name="billing/index.html", context={"user": user, "services": services})
    return render(request, template_name="billing/index.html", context={"user": user})


def pay(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            amount = request.POST.get('amount')
            service = request.POST.get("services")
            _order_id = order_id()
            liqpay = LiqPay(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
            params = {
                'action': 'pay',
                'amount': amount,
                'currency': 'UAH',
                'description': f'Test payment {get_utc_date_time()}',
                'order_id': _order_id,
                'version': '3',
                "result_url": f"http://{HOSTNAME}:8000/billing/"
            }
            signature = liqpay.cnb_signature(params)
            data = liqpay.cnb_data(params)
            service = Service.objects.get(name=service)
            Transaction.objects.create(
                user=request.user,
                service=service,
                amount=amount,
                order_id=_order_id
            )
            # 4242424242424242 Успішна оплата
            payment_info = f"You are going to pay for the {str(service).capitalize()}. Amount {amount} UAH"
            return render(request, template_name="billing/pay.html",
                          context={"data": data, "signature": signature, "payment_info": payment_info})
    return render(request, template_name="account/login.html")


def check_transactions(request):
    update_transactions_statuses(request.user)
    return redirect(f'http://{HOSTNAME}:8000/account')
