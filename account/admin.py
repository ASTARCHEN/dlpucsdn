from django.contrib import admin
from account.models import Profile,Department

# Register your models here.
class profile_admin(admin.ModelAdmin):
    list_display = ('username','number','email','deleted','id')
class department_admin(admin.ModelAdmin):
    list_display = ('name','cn','id')
admin.site.register(Profile, profile_admin)
admin.site.register(Department, department_admin)
