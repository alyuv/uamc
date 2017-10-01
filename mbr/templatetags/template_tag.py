from django import template

register = template.Library()


def get_dict(my_dict, key):
    d = 1
    print(key)
    return my_dict.setdefault(key, None)


@register.filter(name='access')
def access(value, arg):
    # return value[arg]
    try:
        if value.get(arg):
            return value[arg]
        else:
            return False
    except AttributeError:
        d = 1


@register.filter(name='data_form')
def data_form(form, arg):
    # return value[arg]
    return form.cleaned_data[arg]


@register.filter(name='error_index')
def error_index(value, arg):
    if value.get(arg):
        return value[arg]
    else:
        return False

register.filter(get_dict)