from django import template

register = template.Library()

@register.simple_tag
def param_replace(request, **kwargs):
    d = request.GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()
