from django.contrib import admin

from apps.hello.models import MyData


class MyDataAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )

admin.site.register(MyData, MyDataAdmin)
