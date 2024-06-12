from django.contrib import admin
from miniaccounts.models import ProfileInfo

@admin.register(ProfileInfo)
class ProfileInfoAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'acc_name',
        'bio',
        'acc_type',
        'country',
        'gender',
        'dob',
        'email',
        'remail',
        'phone',
        'image',
        'acc_creation_time',
        
    ]
    search_fields = ['user__username', 'email', 'remail', 'phone']
    list_filter = ['gender', 'acc_type', 'acc_name', 'country', 'acc_creation_time']

# Removing unnecessary import statements and comments for clarity



# admin.py

from django.contrib import admin
from miniaccounts.models import EmailVerification

class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
    # Add any other configurations or customizations you want for the admin interface

admin.site.register(EmailVerification, EmailVerificationAdmin)

from django.contrib import admin
from miniaccounts.models import PasswordResetToken

@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
    search_fields = ('user__username', 'token')
    list_filter = ('created_at',)
