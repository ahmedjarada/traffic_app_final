from django.contrib import admin

from .models import User


# Config for User view in admin panel
class UserAdmin(admin.ModelAdmin):
    __module__ = User
    exclude = ('roles',)


# Register user table to admin
admin.site.register(User, UserAdmin)
