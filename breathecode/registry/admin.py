import logging
from django.contrib import admin, messages
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from breathecode.admissions.admin import CohortAdmin
from .models import Asset, AssetTranslation, AssetTechnology, AssetAlias

logger = logging.getLogger(__name__)

def add_gitpod(modeladmin, request, queryset):
    assets = queryset.update(gitpod=True)
add_gitpod.short_description = "Add GITPOD"

def remove_gitpod(modeladmin, request, queryset):
    assets = queryset.update(gitpod=False)
remove_gitpod.short_description = "Remove GITPOD"
# Register your models here.
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug', 'user__email', 'cohort__slug']
    list_display = ('slug', 'title', 'lang', 'asset_type', 'url_path')
    list_filter = ['asset_type', 'lang']
    actions = [add_gitpod, remove_gitpod]
    def url_path(self,obj):
        return format_html(f"<a rel='noopener noreferrer' target='_blank' href='{obj.url}'>open</a>")

# Register your models here.
@admin.register(AssetTranslation)
class AssetTranslationsAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug']
    list_display = ('slug', 'title')

# Register your models here.
@admin.register(AssetTechnology)
class AssetTechnologyAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug']
    list_display = ('slug', 'title')

# Register your models here.
@admin.register(AssetAlias)
class AssetAliasAdmin(admin.ModelAdmin):
    search_fields = ['slug', 'asset']
    list_display = ('slug', 'asset')