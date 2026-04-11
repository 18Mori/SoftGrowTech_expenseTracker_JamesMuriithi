from django import template

register = template.Library()

@register.filter
def sum_list_amount(value):
    """
    Calculates the net total for a list of transactions.
    Adds 'INCOME - EXPENSE'.
    """
    net_total = 0
    for item in value:
        if item.transaction_type == 'INCOME':
            net_total += item.amount
        else:
            net_total -= item.amount
    return net_total
