from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('paypal/execute/', PaymentViewSet.as_view({'get': 'execute_paypal_payment'}), name="execute-paypal"),
]
