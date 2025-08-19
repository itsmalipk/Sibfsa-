from django import template

register = template.Library()

@register.filter
def pkr(amount):
    try:
        amt = int(amount)
    except Exception:
        return amount
    return f"PKR {amt:,.0f}"