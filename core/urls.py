from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/teams/', include('teams.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),          # ADD
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # ADD
    path('', TemplateView.as_view(template_name='index.html')),
]