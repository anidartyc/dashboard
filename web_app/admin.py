from django.contrib import admin
from .models import (
    Client,
    DigitalSolution,
    ClientUser,
    DashboardTag,
    Dashboard,
    HelpContent,
    HelpSection,
    DasboardLog
)
from django.db import models
from tinymce.widgets import TinyMCE
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe
from django.conf import settings
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin



class ClientUserResource(resources.ModelResource):
    class Meta:
        model = ClientUser
        #fields = ('first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'client__name')
        exclude = ('last_login', 'date_joined', 'groups', 'user_permissions')


class DasboardLogResource(resources.ModelResource):
    class Meta:
        model = DasboardLog
        fields = ('user__first_name', 'user__last_name', 'user__email', 'dashboard__name', 'date')


@admin.register(ClientUser)
class ClientUserdmin(ImportExportModelAdmin, DjangoUserAdmin):
    list_display = ("first_name", "last_name","client",  "email", "is_staff", "is_superuser")
    list_filter = ("client__name", "is_staff","client",  "is_superuser")
    search_fields = ("first_name", "last_name","client",  "email")
    resource_class = ClientUserResource
    list_display_links = ("first_name", "last_name", "email")
    list_editable = ("is_staff", "is_superuser", "client",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "updated")
    list_filter = ("name", "created", "updated")
    search_fields = ("name",)
    resource_class = Client
    list_display_links = ("name",)


@admin.register(DigitalSolution)
class DigitalSolutionAdmin(admin.ModelAdmin):
    list_display = ("name", "description", )
    list_filter = ("name",)
    search_fields = ("name", "description")
    resource_class = DigitalSolution
    list_display_links = ("name", "description")


@admin.register(DashboardTag)
class DashboardTagAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "updated")
    list_filter = ("name", "created", "updated")
    search_fields = ("name",)
    resource_class = DashboardTag
    list_display_links = ("name",)


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ("name", "description","digital_solution" , "link", "tags_list")
    list_filter = ("name", "created", "updated")
    search_fields = ("name", "description")
    resource_class = Dashboard
    list_display_links = ("name", "description")

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def link(self, obj):
        return mark_safe('<a href="{url}" target="_blank">Link</a>'.format(url=obj.url))
    
    def tags_list(self, obj):
        return ", ".join([p.name for p in obj.tags.all()])



@admin.register(HelpContent)
class HelpContentAdmin(admin.ModelAdmin):
    list_display = ("tittle", "section")
    list_filter = ("tittle",)
    search_fields = ("tittle", "section")
    resource_class = HelpContent
    list_display_links = ("tittle", "section")
    formfield_overrides = {
    models.TextField: {'widget': TinyMCE()}
    }


@admin.register(HelpSection)
class HelpSectionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    resource_class = HelpSection
    list_display_links = ("name",)



@admin.register(DasboardLog)
class DasboardLogAdmin(ImportExportModelAdmin):
    list_display = ("user", "dashboard", "date")
    list_filter = ("user", "dashboard", "date")
    search_fields = ("user", "dashboard", "date")
    readonly_fields = ('user', 'dashboard', 'date', 'device', 'browser', 'ip')
    resource_class = DasboardLogResource
    list_display_links = ("user", "dashboard", "date")

    def has_add_permission(self, request):
        return False



admin.site.site_header = settings.SITE_CONTEXT["site_name"]
