"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path, re_path
from rest_framework import routers
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
# Only use the DefaultRouter if we have browseable enabled
RouterClass = (
    routers.DefaultRouter
    if settings.ENABLE_BROWSEABLE else
    routers.SimpleRouter)

urlpatterns = [
    # API urls
    # Health Check
    re_path(r'^health/', include('health_check.urls')),

    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Authentication
    path('logout/',
         LogoutView.as_view(template_name=settings.LOGOUT_REDIRECT_URL),
         name='logout'),
    path('api-auth/', include('rest_framework.urls')),


    # Admin
    path('admin/', admin.site.urls),
]

# Admin options
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.index_title = settings.ADMIN_SITE_TITLE
