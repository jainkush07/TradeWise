from import_export import resources
from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UserAdmin(ImportExportModelAdmin):
    list_display = ('id', 'username', 'email')
    # list_filter = ('created_at',)
    resource_class = UserResource
    pass


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class rolesImport(ImportExportModelAdmin):
    pass


class userRolesResource(resources.ModelResource):
    profile_owner = fields.Field(
        column_name='profile_owner', attribute='profile_owner', widget=ForeignKeyWidget(User, 'username'))

    profile_roles = fields.Field(
        column_name='profile_roles', attribute='profile_roles',
        widget=ManyToManyWidget(roles, field='name', separator=','))

    class Meta:
        model = userRoles
        fields = ('profile_owner', 'profile_username', 'referred_by_user', 'profile_roles')


class userRolesImport(ImportExportModelAdmin):
    resource_class = userRolesResource


class UserRoleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('profile_owner__email', 'profile_owner__username')
    filter_horizontal = ('profile_roles',)


admin.site.register(userRoles, UserRoleAdmin)
admin.site.register(roles, rolesImport)

admin.site.register(loginBannerObjects)
admin.site.register(NotificationTemplates)

# @admin.register(userRoles)
# class userRolesImport(ImportExportModelAdmin):
# 	pass
