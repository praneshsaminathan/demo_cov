"""
URL configuration for covid19 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Create a schema view for Swagger documentation
schema_view = get_schema_view(
   openapi.Info(
      title="COVID-19 API",  # Title of the API
      default_version='v1',  # API version
      description="API for COVID-19 Data",  # Description of the API
   ),
   public=True,  # Make the schema public
   permission_classes=(permissions.AllowAny,),  # Allow any permissions
)

urlpatterns = [
    path('', include('app.urls')),  # Include the URLs from the 'app' application
    path('admin/', admin.site.urls),  # Admin site URL
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger documentation URL
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files in development