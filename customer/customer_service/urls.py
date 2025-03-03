from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, AddressViewSet, AccountViewSet, RegisterView, LoginView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'accounts', AccountViewSet)

# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Customer API",
        default_version="v1",
        description="API documentation for Customer, Address, and Account models",
        terms_of_service="https://www.yourwebsite.com/terms/",
        contact=openapi.Contact(email="support@yourwebsite.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    
    # ReDoc UI (alternative API documentation)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
    
    # Raw OpenAPI JSON/YAML schema
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
]
