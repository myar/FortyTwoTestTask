from django import forms
from django.utils.safestring import mark_safe

from .models import MyData


class CalendarWidget(forms.TextInput):
    class Media:
        css = {'all': ('http://code.jquery.com/ui/1.9.1/'
                       'themes/base/jquery-ui.css', ), }

        js = ("http://code.jquery.com/jquery-1.8.2.js",
              "http://code.jquery.com/ui/1.9.1/jquery-ui.js",)

    def __init__(self, params='', attrs=None):
        self.params = params
        super(CalendarWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(CalendarWidget, self).render(name,
                                                      value, attrs=attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
            $('#id_%s').datepicker({%s}); </script>''' % (name, self.params,))


class EditDataForm(forms.ModelForm):
    date_birth = forms.DateField(
        widget=CalendarWidget(params=('dateFormat: "yy-mm-dd", '
                                      'changeYear: true, firstDay: 1')))

    class Meta:
        model = MyData
