from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter(trailing_slash=False)
router.register("", views.AuthenticationView, basename="Authentication")

urlpatterns = [
    path("auth/", include(router.urls)),
]
