from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag()
def edit_link(obj):
    """
    This is simple tag, how accepts any object and renders the link to its
    admin edit page
    """
    # but need in view render value obj
    try:
        url = reverse('admin:%s_%s_change' %
                      (obj._meta.app_label, obj._meta.module_name),
                      args=[obj.id])
    except:
        url = "#"
    return '<a href="%s">(admin)</a>' % url
