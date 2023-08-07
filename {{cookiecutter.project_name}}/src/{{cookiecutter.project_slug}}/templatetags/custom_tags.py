import datetime
from django import template

# Creating the register instance by initializing it with the library instance.
register = template.Library()

#syntax
"""
def my_tags(arg):
    return arg
"""
# A function that returns the current date.
@register.simple_tag(name='current_date')
def current_date(format):
    return datetime.datetime.now().strftime(format)