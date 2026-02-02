from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class AccountAdmin(UserAdmin):
    model=Account
    list_display=('first_name','last_name','email','date_joined',)
    list_filter = ('is_admin', 'is_active')
    fieldsets=(
        (None,{'fields':('email','username','password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superadmin', 'is_active')}),
        ('Important Dates', {'fields': ('date_joined', 'last_login')}),
    )
    readonly_fields = ('date_joined', 'last_login')
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Account,AccountAdmin)