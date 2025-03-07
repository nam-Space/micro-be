from django.urls import path
from .views import get_cart, add_to_cart, remove_from_cart, update_cart_item
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Cart API",
        default_version="v1",
        description="API documentation for Cart and CartItem models",
        terms_of_service="https://www.yourwebsite.com/terms/",
        contact=openapi.Contact(email="support@yourwebsite.com"),  # FIXED EMAIL STRING
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('<int:customer_id>/', get_cart, name="get_cart"),
    path('cart/', add_to_cart, name="add_to_cart"),
    path('<int:customer_id>/remove/<str:product_type>/<int:product_id>/', remove_from_cart, name="remove_from_cart"),
    path('cart-update/', update_cart_item, name="update_cart_item"),
    
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),  
]
