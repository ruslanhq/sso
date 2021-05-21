from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import (
    UserViewSet, CustomTokenObtainPairView, ChangePasswordView, EcomInfoView
)

app_name = 'authentication'

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('ecom_info', EcomInfoView, basename='add_info')

urlpatterns = [
    path('', include(router.urls)),
    path('change_password/', ChangePasswordView.as_view()),
    path('token/', CustomTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]

urlpatterns += router.urls
