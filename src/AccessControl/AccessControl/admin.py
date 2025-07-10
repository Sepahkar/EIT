from django.contrib import admin
import AccessControl.models as A


admin.site.site_header = "مدیریت سیستم دسترسی"
admin.site.index_title = "سیستم دسترسی شرکت فناوران"


class AppInLine(admin.TabularInline):
    model = A.App


@admin.register(A.System)
class Project(admin.ModelAdmin):
    class Meta:
        model = A.System

    inlines = [AppInLine]
    list_display = ("Title",)
    search_fields = ("Title",)
    list_filter = ("PortNumber",)


class VariableValueRelatedInLine(admin.TabularInline):
    model = A.VariableValueRelated


class PermissionInLine(admin.TabularInline):
    model = A.Permission


class AppURLInLine(admin.TabularInline):
    model = A.AppURL


@admin.register(A.App)
class Project(admin.ModelAdmin):
    class Meta:
        model = A.App

    inlines = [AppURLInLine, PermissionInLine]
    list_display = ("Title",)
    search_fields = ("Title",)


class RelatedPermissionAPPURLInLine(admin.TabularInline):
    model = A.RelatedPermissionAPPURL


@admin.register(A.AppURL)
class AppURL(admin.ModelAdmin):
    class Meta:
        model = A.AppURL

    inlines = [RelatedPermissionAPPURLInLine]
    list_display = ("AppCode",)


@admin.register(A.PermissionVariableValue)
class PermissionVariableValue(admin.ModelAdmin):
    class Meta:
        model = A.PermissionVariableValue

    inlines = [
        VariableValueRelatedInLine,
    ]
    list_display = ("App",)
    search_fields = ("App",)


@admin.register(A.GroupUser)
class GroupUser(admin.ModelAdmin):
    class Meta:
        model = A.GroupUser


class GroupUserInLine(admin.TabularInline):
    model = A.GroupUser


@admin.register(A.PermissionGroup)
class PermissionGroup(admin.ModelAdmin):
    class Meta:
        model = A.PermissionGroup

    inlines = [GroupUserInLine]


admin.site.register(A.RelatedPermissionAPPURL)
admin.site.register(A.AppPermissionType)
admin.site.register(A.UserRoleGroupPermission)
admin.site.register(A.PermissionVariable)
admin.site.register(A.Permission)
