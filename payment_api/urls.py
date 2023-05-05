"""payment_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
 
from .views import index


urlpatterns = [
    path('admin/', admin.site.urls), 
    path("", include('app_authentication.urls')),
    path("", include('app_payment.urls')),
]

urlpatterns_swagger = [
    # YOUR PATTERNS
    # Optional UI:
    path('api/docs/', SpectacularSwaggerView.as_view(), name='swagger-ui'),
    path('api/json/', SpectacularAPIView.as_view(), name='schema'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('', index, name='index'),
]

urlpatterns += urlpatterns_swagger

