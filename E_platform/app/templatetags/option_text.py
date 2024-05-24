# myapp/templatetags/option_text.py
from django import template

register = template.Library()

@register.filter
def get_option_text(option_number, question):
    if option_number == '1':
        return question.option1
    elif option_number == '2':
        return question.option2
    elif option_number == '3':
        return question.option3
    elif option_number == '4':
        return question.option4
    return ''
