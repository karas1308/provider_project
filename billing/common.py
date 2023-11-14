from liqpay import LiqPay

from account.models import User
from billing.models import Transaction
from config import LIQPAY_PRIVATE_KEY, LIQPAY_PUBLIC_KEY


def check_payment_status(order_id):
    liqpay = LiqPay(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
    res = liqpay.api("request", {
        "action": "status",
        "version": "3",
        "order_id": order_id
    })
    return res


def update_transactions_statuses(user):
    transactions = Transaction.objects.filter(user=user, is_expired=False, successful_payment=False)
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
        transactions = Transaction.objects.filter(user=user, order_id__in=order_ids)
        transactions.update(is_expired=True, successful_payment=True)
        transactions = Transaction.objects.filter(user=user, order_id__in=failed_order_ids)
        transactions.update(is_expired=True, successful_payment=False)
        user_info = User.objects.filter(id=user.id)
        user_info.update(balance=user_info[0].balance + transaction_amount)
