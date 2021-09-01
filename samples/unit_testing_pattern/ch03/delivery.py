import datetime as dt


def is_delivery_valid(delivery: dt.datetime) -> bool:
    return delivery >= dt.datetime.now() + dt.timedelta(days=1.99)
