"""
URL configuration for Chemical Equipment Parameter Visualizer.
Serves both API and React frontend from single deployment.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve React frontend for all other routes (SPA catch-all)
# This must be last - catches all non-API routes and serves React
urlpatterns += [
    re_path(r'^(?!api|admin|static|media).*$', TemplateView.as_view(template_name='index.html')),
]
