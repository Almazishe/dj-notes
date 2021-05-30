from django.contrib import admin
from rest_framework_simplejwt import token_blacklist
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True

admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)
