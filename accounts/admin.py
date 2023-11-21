from django.contrib import admin

# Register your models here.

# Style User Admin while inheriting base design
from django.contrib.auth.admin import UserAdmin
from .models import User, VerificationCount

class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'role','first_name', 'role']
    search_fields = ('email', 'username','role','is_staff','groups')


class VerificationCountAdmin(admin.ModelAdmin):
    list_display = ['email', 'count', 'last_attempt']
    search_fields = ('email', 'count', 'last_attempt')

admin.site.register(User, CustomUserAdmin)
admin.site.register(VerificationCount, VerificationCountAdmin)

