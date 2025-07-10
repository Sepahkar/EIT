from django.contrib import admin
import Systems.models as S

admin.site.site_header = "مدیریت سیستم میزکار"
admin.site.site_title = "سیستم میزکار"
admin.site.index_title = "سیستم میزکار"



@admin.register(S.SystemCategory)
class SystemCategory(admin.ModelAdmin):
    list_display = ('Title',)
    search_fields = ('Title',)


@admin.register(S.SystemCategoryURL)
class SystemCategoryURL(admin.ModelAdmin):
    list_display = ('SystemCategory',)
