from django.contrib import admin

from .models import Account

from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.models import Group
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display        = ("email", "first_name", "username", "last_login", "date_joined", "is_active")
    ordering            = ("date_joined",)
    list_display_links  = ("email", "first_name")
    readonly_fields     = ("last_login", "date_joined")

    filter_horizontal   = ()
    list_filter         = ()
    fieldsets           = ()



admin.site.register(Account, AccountAdmin)
admin.site.unregister(Group) #grubu gizlemek için ekledik
