from rest_framework.permissions import BasePermission
from rest_framework import authentication
import jwt, logging
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions

logging = logging.getLogger('django')

SAFE_METHODS = ['GET']
SIGNUP_SAFE_METHODS = ['GET', 'POST']
 

class AllowAnyOnGetMethod(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or (request.user and request.user.is_authenticated and request.user.is_superuser):
            return True
        return False
    

class BearerAuthScheme(OpenApiAuthenticationExtension):
    target_class = JWTAuthentication
    name = "bearerAuth"  # name used in the schema

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "name": "Authorization",
            "in": "header",
        }