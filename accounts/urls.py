from django.urls import include, path
from .views import RegisterView, CurrentUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from .views import AddressViewSet

router = DefaultRouter()
router.register("addresses", AddressViewSet, basename="addresses")

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("me/", CurrentUserView.as_view(), name="current-user"),
    path("", include(router.urls)),
]