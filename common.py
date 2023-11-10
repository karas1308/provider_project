import uuid
from datetime import datetime, timedelta


def order_id():
    return str(uuid.uuid4())


def get_utc_date_time(amount_of_days=0, hours=0, minutes=0, seconds=0, date_format="%Y-%m-%dT%H:%M:%SZ"):
    today_date = datetime.utcnow()
    today_date += timedelta(days=amount_of_days, hours=hours, minutes=minutes, seconds=seconds)
    return today_date.strftime(date_format)
