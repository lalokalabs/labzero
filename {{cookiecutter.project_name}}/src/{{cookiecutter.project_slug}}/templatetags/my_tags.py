import datetime
from django import template
# Creating the register instance by initializing it with the Library instance.
register = template.Library()

"""
Syntax

def my_tags(arg):
    return arg
"""
# example
# A function that returns the current date.
@register.simple_tag(name='current_date')
def current_date(format):
    return datetime.datetime.now().strftime(format)
