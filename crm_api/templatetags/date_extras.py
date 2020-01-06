from django import template
import datetime
import math

register = template.Library()


@register.simple_tag
def last_year():
    now = datetime.datetime.now()
    return str(now.year - 1)


@register.simple_tag
def last_month(with_year=False):
    now = datetime.datetime.now()
    month = now.month - 1 if now.month > 1 else 12
    ret = f'{month}'
    if with_year:
        ret += f'/{now.year if now.month > 1 else now.year - 1}'
    return ret


@register.simple_tag
def get_quartal():
    return str(math.ceil(datetime.datetime.now().month / 3))
