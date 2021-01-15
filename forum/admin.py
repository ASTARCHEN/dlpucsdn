from django.contrib import admin
from forum.models import Topic


# Register your models here.
class ForumAdmin(admin.ModelAdmin):
    list_display = ('title', 'auth', 'time_created', 'reply_count', 'id')


admin.site.register(Topic, ForumAdmin)
