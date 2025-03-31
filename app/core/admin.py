"""
Django admin customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id'] # Users will be displayed in order of their ID.
    list_display = ['email', 'name'] # The admin list page will show only email and name, instead of Django’s default display.
    # fieldsets is used to group and organize fields on the user edit page.
    #Each fieldset consists of: 1)A title (which can be None if no title is needed).
    # 2)A dictionary { 'fields': (...) } listing the fields that belong to that section.

    # gettext_lazy is Django’s internationalization (i18n) function. It allows the section titles (Permissions, Important dates)
    # to be translated into different languages if needed.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login', )}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser'
            )
        }),
    )

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
admin.site.register(models.Tag)

