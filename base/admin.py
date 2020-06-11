from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from base.models import Transaction, User


class HackUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'balance', 'notes', 'picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'balance', 'notes', 'picture')}),
    )


class TransationAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'created')


admin.site.register(User, HackUserAdmin)
admin.site.register(Transaction, TransationAdmin)
