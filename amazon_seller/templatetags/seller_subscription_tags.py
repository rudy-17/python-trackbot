from django import template
register = template.Library()
from datetime import timedelta

@register.filter(name='checkSandbox')
def checkSandbox(value, *args):
    print(value)
    if value == 'active':
        return True
    else:
        return False
