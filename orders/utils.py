import datetime
import simplejson as json


def generate_order_number(pk):
    current_date_time = datetime.datetime.now().strftime('%Y%m%d%H%M')
    return f"{current_date_time}{pk}"


def order_total_by_vendor(order, vendor):
    total_data = json.loads(order.total_data)
    data = total_data.get(str(vendor.id))
    subtotal = 0
    tax = 0
    tax_dict = {}

    for key, val in data.items():
        subtotal += float(key)
        val = val.replace("'", '"')
        val = json.loads(val)
        tax_dict.update(val)


        for i in val:
            for j in val[i]:
                tax += float(val[i][j])
    graand_total = float(subtotal) + float(tax)
    context = {
        'subtotal': subtotal,
        'tax_dict': tax_dict,
        'grand_total': graand_total,
    }
    return context