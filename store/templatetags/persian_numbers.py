from django import template

register = template.Library()


@register.filter
def trans_number(value):
    value = str(value)
    persian_numbers = '۱۲۳۴۵۶۷۸۹۰'
    english_numbers = '1234567890'
    translation_table = str.maketrans(english_numbers, persian_numbers)
    return value.translate(translation_table)
