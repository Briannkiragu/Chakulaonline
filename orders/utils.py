import datetime


def generate_order_number(pk):
    current_date_time = datetime.datetime.now().strftime('%Y%m%d%H%M')
    return f"{current_date_time}{pk}"