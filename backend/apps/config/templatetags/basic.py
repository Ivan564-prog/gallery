from django import template


register = template.Library()


@register.filter(name="format_number")
def format_number(value):
    try:
        if value % 1 == 0:
            return '{:,.0f}'.format(float(value)).replace(',', ' ')
        else:
            return '{:,.1f}'.format(float(value)).replace(',', ' ')
    except:
        pass

@register.filter(name="call")
def format_number(obj, method):
    return getattr(obj, method)