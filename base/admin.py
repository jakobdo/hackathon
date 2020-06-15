from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from base.models import Deposit, DepositHistory, Transaction, User


class DepositAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'amount')


class DepositHistoryAdmin(admin.ModelAdmin):
    list_display = ('deposit', 'user')


class HackUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'notes', 'picture', 'leaderboard')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'notes', 'picture', 'leaderboard')}),
    )


class TransationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'amount', 'created')


admin.site.register(Deposit, DepositAdmin)
admin.site.register(DepositHistory, DepositHistoryAdmin)
admin.site.register(User, HackUserAdmin)
admin.site.register(Transaction, TransationAdmin)
