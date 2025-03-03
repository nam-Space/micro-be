from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, PhoneViewSet, ClothesViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'phones', PhoneViewSet)
router.register(r'clothes', ClothesViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
