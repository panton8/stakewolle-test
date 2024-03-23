from django.contrib import admin
from core.user.models import ReferralCode, User


@admin.register(ReferralCode)
class RefCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'valid_until', 'creator')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('public_id', 'username', 'first_name', 'last_name', 'email', 'referral_code', 'bonus', 'is_active', 'is_staff', 'is_superuser', 'created', 'updated')