from django import template

# Create the register instance by initializing it with the Library instance.
register = template.Library()

def my_tags(arg):
    return arg
