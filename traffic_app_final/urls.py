"""traffic_app_final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.http import HttpResponse
from django.urls import path, include
from user.views import delete_user
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .swagger_api_generator import SwaggerAPISchemaGenerator


# from rest_framework.schemas import get_schema_view as schema_view
def home(request):
    return HttpResponse(
        '<title> Traffic App</title><h1>Welcome to Traffic App API</h1><p>Last update in [12-12-2020]</p>')


urlpatterns = [path('', home),
               path('admin/', admin.site.urls),
               path('account/', include('user.urls')),
               path('delete_account/', delete_user), ]

sawgger_view = get_schema_view(
    openapi.Info(
        title="Traffic App API",
        default_version='v1',
        description="This is a traffic RESTFUL App",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=urlpatterns,
    generator_class=SwaggerAPISchemaGenerator
)

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$', sawgger_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', sawgger_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', sawgger_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

