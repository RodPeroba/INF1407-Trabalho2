"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from django.urls.conf import include
from rest_framework import routers, permissions
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view as yasg_schema_view
from drf_yasg import openapi
from main import views

# TODO Adicionar a url do site no schema_view quando for colocar no ar
schema_view = yasg_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation for the project",
        contact=openapi.Contact(email="rodperoba@hotmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin site
    path('batata/', admin.site.urls),

    #Apps
    path('comprador/', include('comprador.urls')),
    path('vendedor/', include('vendedor.urls')),

    # Documentação da API
    path('docs/',include_docs_urls(title='Documentação da API')),
    path('swagger/',schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    path('api/v1/',include(routers.DefaultRouter().urls)),
    path('openapi',get_schema_view(title="API para loja e e-commerce",description="API para obter dados da loja de e-commerce",),name='openapi-schema'),

    # Homepage
    path('',views.HomePage.as_view(), name='homepage'),
]
