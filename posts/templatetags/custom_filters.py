from django import template

register = template.Library()


@register.filter()
def censorship(value):
    word = 'reallybadword'



    if not isinstance(value, str):
        raise ValueError(f"String is expected, got {type(value)}")

    for w in value.split():
        if w.lower() == word:
            value = value.replace(w, f"{w[0]}{'*' * (len(w) - 1)}")

    return value
