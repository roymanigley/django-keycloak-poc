import sys

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

handler404 = "config.views.page_not_found_view"
handler403 = "config.views.page_permission_denied_view"
handler500 = "config.views.page_unexpected_error_view"

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),

    path('auth/', include('allauth.urls')),

    path('403/', TemplateView.as_view(template_name='403.html'), name='404'),
    path('404/', TemplateView.as_view(template_name='404.html'), name='404'),
    path('500/', TemplateView.as_view(template_name='500.html'), name='404'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    if 'test' not in sys.argv:
        from debug_toolbar.toolbar import debug_toolbar_urls
        urlpatterns += debug_toolbar_urls()
