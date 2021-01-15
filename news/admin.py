from django.contrib import admin
from news.models import List


# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'auth', 'url', 'time_created', 'department_name', 'id')


admin.site.register(List, NewsAdmin)
