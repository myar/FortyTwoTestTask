from django.contrib import admin

from apps.hello.models import MyData, StorageRequests


class MyDataAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )

admin.site.register(MyData, MyDataAdmin)


class StorageRequestsAdmin(admin.ModelAdmin):
    list_display = ('host', 'req_date')

admin.site.register(StorageRequests, StorageRequestsAdmin)
