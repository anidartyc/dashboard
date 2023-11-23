"""
URL configuration for data_dashboard_bi project.

"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls), 
    path('', include('web_app.urls')), 
    path("accounts/", include("django.contrib.auth.urls")), 
    path('accounts/', include('allauth.urls')),
    #path('accounts/', include('allauth.socialaccount.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
