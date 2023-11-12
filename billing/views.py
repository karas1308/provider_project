from django.shortcuts import redirect, render
from liqpay import LiqPay

from account.models import User
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
    transactions = Transaction.objects.filter(user=request.user, is_expired=False, successful_payment=False)
    order_ids = []
    failed_order_ids = []
    transaction_amount = 0
    if transactions:
        for transaction in transactions:
            payment_status = check_payment_status(transaction.order_id)
            if payment_status["status"] == "success":
                order_ids.append(transaction.order_id)
                transaction_amount += transaction.amount
            if payment_status["status"] != "success":
                failed_order_ids.append(transaction.order_id)
        transactions = Transaction.objects.filter(user=request.user, order_id__in=order_ids)
        transactions.update(is_expired=True, successful_payment=True)
        transactions = Transaction.objects.filter(user=request.user, order_id__in=failed_order_ids)
        transactions.update(is_expired=True, successful_payment=False)
        user_info = User.objects.filter(id=request.user.id)
        user_info.update(balance=user_info[0].balance + transaction_amount)
    return redirect(f'http://{HOSTNAME}:8000/account')


def check_payment_status(order_id):
    liqpay = LiqPay(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
    res = liqpay.api("request", {
        "action": "status",
        "version": "3",
        "order_id": order_id
    })
    return res
