from django import template
register = template.Library()
from datetime import timedelta

@register.filter(name='addDays')
def addDays(start, days, *args):
    return str((start + timedelta(days=days)).date())

@register.filter(name='dateToString')
def dateToString(date, *args):
    return str(date.date())
