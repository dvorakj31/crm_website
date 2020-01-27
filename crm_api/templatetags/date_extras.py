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


def _get_deadline_day(month):
    day = 25
    now = datetime.datetime.now()
    year = now.year
    if month < now.month:
        month = 1
        year += 1
    if month == 12:
        day = 27
    date = datetime.date(year, month, day)
    if date.weekday() > 4:
        day = day + 7 - date.weekday()
    return day


@register.simple_tag
def get_vat_deadline(is_monthly):
    now = datetime.datetime.now()
    if is_monthly:
        month = now.month + 1
        if month > 12:
            month %= 12
    else:
        month = 1
        if 1 <= now.month <= 4:
            month = 4
        elif 5 <= now.month <= 7:
            month = 7
        elif 8 <= now.month <= 10:
            month = 10
        if now.day > 25 and month == now.month:
            month = (month + 3) % 12
    day = _get_deadline_day(month)
    date = f"{day}. {month}."
    return date
